from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from reservas.models import Room, BookingState, BookingType, RoomType, Checkout
from accesos.models import Usr, Perfil
from administracion.choices import TIPO_DE_IDENTIFICACION, GENERO, REASON_CHECKOUT
from django.views.generic import ListView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from administracion.forms import RoomForm, DocumentForm, NoticiaForm
from tour_package.forms import TourForm
from .models import Publicidad
from .forms import PublicidadForm
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout
import pytz
from rest_framework import generics
from rest_framework import views
from rest_framework.response import Response
from django.conf import settings
from django.core.mail import send_mail

# from datetime import date
# from datetime import datetime
import dateutil.parser

from django.core.files.storage import FileSystemStorage
from django.db.models import Max

import datetime

from django.http import JsonResponse

# Modelos
from accesos.models import Usr
from accesos.models import Perfil
from reservas.models import Booking
from noticias.models import Noticia

from tour_package.models import Tour_Package


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/administracion/')
    else:
        form = DocumentForm()
    return render(request, 'rooms/documento_form.html', {
        'form': form
    })


def index(request):
    if('success_login' in request.session and request.session['success_login']):
        return render(request, 'index-admin.html')
    return redirect('/administracion/login')


def reservas(request):
    template_name = 'reservas/reservas-admin.html'
    return render(request, template_name)


class RoomList(ListView):
    model = Room
    context_object_name = 'rooms'
    template_name = 'rooms/index_rooms.html'


def room_create_form(request):
    print("Entra a room_create_form")
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/administracion/')
    else:
        form = RoomForm()
    return render(request, 'rooms/create_room.html', {
        'form': form
    })


class RoomCreate(CreateView):
    model = Room
    form_class = RoomForm
    template_name = "rooms/create_room.html"

    success_url = reverse_lazy("administracion:room_list")


def upload_image_room(request):
    print("Entra a upload_image_room")
    if request.method == 'POST':
        file = request.FILES['path_image']
        form = RoomForm(request.POST, request.FILES)
        fs = FileSystemStorage()

        if form.is_valid():
            numero_cuarto = get_last_item_id() + 1
            nombre_imagen = "imagen_cuarto_" + \
                str(numero_cuarto) + '.' + (file.name.split('.'))[1]
            fs.save(nombre_imagen, file)
            form.save()
            return redirect('/administracion/')
    else:
        form = RoomForm()

    return render(request, 'rooms/index_rooms.html', {'form': form})


def get_last_item_id():
    if len(Room.objects.all()) > 0:
        return Room.objects.all().order_by("-id")[0].id
    else:
        return 0


class RoomEdit(UpdateView):

    model = Room
    context_object_name = 'room'
    template_name = 'rooms/room_edit.html'
    form_class = RoomForm

    def get_object(self):
        id_ = self.kwargs.get("id_room")
        return get_object_or_404(Room, id=id_)

    success_url = reverse_lazy("administracion:room_list")


class RoomDelete(DeleteView):
    model = Room
    success_url = reverse_lazy("administracion:room_list")
    template_name = 'rooms/room_delete_form.html'

    def get_object(self):
        id_ = self.kwargs.get("id_room")
        return get_object_or_404(Room, id=id_)

###Accesos de administrador###


def login(request):
    if request.method == 'POST':
        print("Post")
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email is None or password is None:
            # return HttpResponse("Por favor ingrese el email y contrasena!")
            request.session['success_login'] = False
            return redirect('/administracion/login')
        try:
            usr = Usr.objects.get(email=email, is_admin=True)
            # print(password)
            # print(usr.password)
            if(check_password(password, usr.password)):
                perfil = Perfil.objects.get(usr_id_id=usr.id)
                request.session['success_login'] = True
                request.session.modified = True
                # print(perfil.name)    Para verificar si toma el perfil
                customer_json = {
                    'customer_id': perfil.id,
                    'name': perfil.name,
                    'last_name': perfil.last_name,
                    'date_birth': str(perfil.date_birth),
                    'email': usr.email,
                    'username': usr.username
                }

                print(customer_json)
                request.session['customer'] = customer_json

                return redirect('/administracion')
            else:
                print("entra a false")
                request.session['success_login'] = False
                return redirect('/administracion/login')

        except Exception as error:
            print(error)
            request.session['success_login'] = False
            return redirect('/administracion/login')
    else:
        if('success_login' in request.session and request.session['success_login']):
            return redirect('/administracion')
        return render(request, 'accesos/login.html')


def logout_admin(request):
    logout(request)
    return redirect('/administracion/login')

###Accesos de administrador###

###Administracion de administradores###


def administradores(request):
    admin_list = []
    out_queries = Perfil.objects.raw('''
        select ap.id, ap.name, ap.last_name, au.email, au.is_removed
        from accesos_perfil as ap, accesos_usr as au
        where ap.usr_id_id = au.id
        and au.is_admin = true
        and ap.is_removed = false
        and au.is_removed = false;
    ''')

    for e in out_queries:
        print(e)
        admin_list.append(e)

    print(admin_list)
    return render(request, 'admin_administradores/administradores.html', {'administradores': admin_list,
                                                                          'choices': TIPO_DE_IDENTIFICACION, 'genero': GENERO})


def administrador_eliminacion(request, id):
    perfil = Perfil.objects.get(id=id)
    usr = Usr.objects.get(id=perfil.usr_id_id)

    perfil.is_removed = True
    perfil.update_date = datetime.datetime.now()
    usr.is_removed = True
    usr.update_date = datetime.datetime.now()

    perfil.save()
    usr.save()

    return redirect('/administracion/administradores')


def administrador_edicion(request, id):
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('nombres')
        last_name = request.POST.get('apellidos')
        date_birth = request.POST.get('fecha_nacimiento')
        email = request.POST.get('email')
        phone = request.POST.get('telf')
        is_removed = request.POST.get('is_removed')
        cedula = request.POST.get('documento')
        doc_type = request.POST.get('dropwdown-docs')
        genero = request.POST.get('dropwdown-generos')

        perfil = Perfil.objects.get(id=id)
        usr = Usr.objects.get(id=perfil.usr_id_id)

        perfil.name = name
        perfil.last_name = last_name
        perfil.date_birth = date_birth
        perfil.phone = phone
        cedula = cedula,
        doc_type = doc_type,
        genero = genero

        perfil.save()
        usr.save()

        return redirect('/administracion/administradores')

    else:
        admin = list(Perfil.objects.values('id', 'name', 'last_name', 'phone',
                                           'date_birth', 'usr_id_id__email', 'is_removed', 'cedula', 'doc_type', 'genero').filter(id=id))
        admin[0]['date_birth'] = admin[0]['date_birth'].strftime("%Y-%m-%d")
        print(admin)

        return render(request, 'admin_administradores/administrador_edicion.html', {
            'administrador': admin[0],
            'docs': TIPO_DE_IDENTIFICACION,
            'generos': GENERO
        })


def administrador_nuevo(request):
    if request.method == "POST":
        print(request.POST)
        name = request.POST.get('nombres')
        last_name = request.POST.get('apellidos')
        date_birth = request.POST.get('fecha_nacimiento')
        email = request.POST.get('email')
        phone = request.POST.get('telf')
        password_hash = make_password('Admin2019')
        cedula = request.POST.get('documento')
        doc_type = request.POST.get('dropwdown-docs')
        genero = request.POST.get('dropwdown-generos')

        usr = Usr(
            username=email.split('@')[0],
            email=email,
            password=password_hash,
            is_admin=True
        )

        usr.save()

        perfil = Perfil(
            usr_id=usr,
            name=name,
            last_name=last_name,
            date_birth=date_birth,
            phone=phone,
            cedula=cedula,
            doc_type=doc_type,
            genero=genero
        )

        perfil.save()

        return redirect('/administracion/administradores')

    else:
        return render(request, 'admin_administradores/administrador_nuevo.html', {
            'docs': TIPO_DE_IDENTIFICACION,
            'generos': GENERO})


###Administracion de administradores###

###Habitaciones disponibles###


###Habitaciones disponibles###
def habitaciones_disponibilidad(request):
    room_list = []
    room_list = list(Room.objects.values('id', 'descripcion', 'calificacion', 'num_camas',
                                         'num_adultos', 'num_ninos', 'precio', 'disponible', 'id_roomtype_id__nombre'))
    print(room_list)
    return render(request, 'habitaciones_disponibles/habitaciones_disponibles.html', {'habitaciones_disponibles': room_list})


###Administracion de reservas###


def lista_reservas(request):
    print("Entraaaaa a listar")
    reservas_list = []
    out_queries = Booking.objects.raw('''
        select b.id, b.check_in_date, b.check_out_date, p.name, p.last_name, p.cedula, r.nombre, r.numero
        from reservas_booking as b, accesos_perfil as p, reservas_room as r
        where b.customer_id_id = p.id and b.room_id_id = r.id
    ''')
    print(out_queries)
    for e in out_queries:
        print(e)
        reservas_list.append(e)
        e.check_in_date = e.check_in_date.strftime("%Y-%m-%d %I:%M %p")
        e.check_out_date = e.check_out_date.strftime("%Y-%m-%d %I:%M %p")
        if(e.fecha_ingresado is None):
            e.fecha_ingresado = "-"
        else:
            e.fecha_ingresado = e.fecha_ingresado.strftime("%Y-%m-%d %I:%M %p")
        if(e.fecha_salida is None):
            e.fecha_salida = "-"
        else:
            e.fecha_salida = e.fecha_salida.strftime("%Y-%m-%d %I:%M %p")

    return render(request, 'reservas/reservas-admin.html', {'lista_reservas': reservas_list})


def eliminar_reserva(request, id):
    Booking.objects.filter(id=id).delete()
    return render(request, 'reservas/reservas-admin.html', {'lista_reservas': reservas_list})


def agregar_reserva(request):
    if request.method == 'POST':                
        print(request.POST)
        json_post = request.POST
        if(json_post['id_cliente']!=''):
            
            #Obtener el perfil del usuario que hace la reserva
            perfil_model = get_object_or_404(Perfil, id=json_post['id_cliente'])

            #Obtener el estado registrado de un booking
            bookingstate_model = get_object_or_404(BookingState, name="Registrada")

            #Obtener la habitacion
            room_model = get_object_or_404(Room, id=json_post['id_habitacion'])
            
            str_fechain = json_post['fechain_form'].split(" ")[0].split('/')[2]+"-"+json_post['fechain_form'].split(" ")[0].split('/')[0]+"-"+json_post['fechain_form'].split(" ")[0].split('/')[1]+" "+json_post['fechain_form'].split(" ")[1]+" "+json_post['fechain_form'].split(" ")[2]
            str_fechasal = json_post['fechasal_form'].split(" ")[0].split('/')[2]+"-"+json_post['fechasal_form'].split(" ")[0].split('/')[0]+"-"+json_post['fechasal_form'].split(" ")[0].split('/')[1]+" "+json_post['fechasal_form'].split(" ")[1]+" "+json_post['fechasal_form'].split(" ")[2]
            print(str_fechain)
            print(str_fechasal)
            fechain_datetime = datetime.datetime.strptime(str_fechain, '%Y-%m-%d %I:%M %p')
            fechasal_datetime = datetime.datetime.strptime(str_fechasal, '%Y-%m-%d %I:%M %p')
            dif = fechasal_datetime - fechain_datetime
            booking_model = Booking(
                customer_id=perfil_model,
                room_id=room_model,
                state_id=bookingstate_model,
                check_in_date=fechain_datetime,
                check_out_date=fechasal_datetime,
                num_adultos=int(json_post['num_adultos_form']),
                num_ninos=int(json_post['num_ninos_form']),
                total_to_pay=float(json_post['total_pagar_form']),
                no_nights=dif.days
            )
            booking_model.save()

            return redirect('/administracion/lista_reservas')
        else:

            #Registro del nuevo cliente
            password_hash = make_password(json_post['documento_form'])            
            usr_model = Usr(
                username=json_post['email_form'].split('@')[0],
                email=json_post['email_form'],
                password=password_hash,
                is_admin=False
            )

            usr_model.save()

            perfil_model = Perfil(
                usr_id=usr_model,
                name=json_post['nombres_form'],
                last_name=json_post['apellidos_form'],
                date_birth=json_post['fecha_nacimiento_form'],
                phone=json_post['telf_form'],
                cedula=json_post['documento_form'],
                doc_type=json_post['tipo_documento_form'],
            )

            perfil_model.save()

            #Obtener el estado registrado de un booking
            bookingstate_model = get_object_or_404(BookingState, name="Registrada")

            #Obtener la habitacion
            room_model = get_object_or_404(Room, id=json_post['id_habitacion'])
            
            str_fechain = json_post['fechain_form'].split(" ")[0].split('/')[2]+"-"+json_post['fechain_form'].split(" ")[0].split('/')[0]+"-"+json_post['fechain_form'].split(" ")[0].split('/')[1]+" "+json_post['fechain_form'].split(" ")[1]+" "+json_post['fechain_form'].split(" ")[2]
            str_fechasal = json_post['fechasal_form'].split(" ")[0].split('/')[2]+"-"+json_post['fechasal_form'].split(" ")[0].split('/')[0]+"-"+json_post['fechasal_form'].split(" ")[0].split('/')[1]+" "+json_post['fechasal_form'].split(" ")[1]+" "+json_post['fechasal_form'].split(" ")[2]
            print(str_fechain)
            print(str_fechasal)
            fechain_datetime = datetime.datetime.strptime(str_fechain, '%Y-%m-%d %I:%M %p')         
            fechasal_datetime = datetime.datetime.strptime(str_fechasal, '%Y-%m-%d %I:%M %p') 
            dif = fechasal_datetime - fechain_datetime
            booking_model = Booking(
                customer_id=perfil_model,
                room_id=room_model,
                state_id=bookingstate_model,
                check_in_date=fechain_datetime,
                check_out_date=fechasal_datetime,
                num_adultos=int(json_post['num_adultos_form']),
                num_ninos=int(json_post['num_ninos_form']),
                total_to_pay=float(json_post['total_pagar_form']),
                no_nights=dif.days
            )
            booking_model.save()

            return redirect('/administracion/lista_reservas')
    else:
        print("entra a else de agregar_reserva")
        room_type_list = list(RoomType.objects.values('id', 'nombre'))
        print(room_type_list)
        print(TIPO_DE_IDENTIFICACION)
        return render(request, 'reservas/addreserva.html', {'choices_id': TIPO_DE_IDENTIFICACION, 'room_type': room_type_list})


def buscarcliente(request):
    ced = request.GET.get('cedula', None)
    doc_type = request.GET.get('tipo_documento', None)
    """ print("cedula"+ced) """
    is_taken = Perfil.objects.filter(
        cedula__iexact=ced, doc_type=doc_type).exists()
    if(is_taken):
        user = Perfil.objects.filter(cedula=ced)[0]
        u = Usr.objects.filter(id=user.usr_id_id)[0]
        data = {
            'existe': is_taken,
            'id': user.id,
            'nombres': user.name,
            'apellidos': user.last_name,
            'fecha_nacimiento': user.date_birth.strftime("%Y-%m-%d"),
            'telfono': user.phone,
            'email': u.email
        }
        print(data)
    else:
        data = {
            'existe': False
        }
    return JsonResponse(data)

def buscarhabitaciones(request):
    try:
        json_get = request.GET

        #Buscar habitaciones con campo disponible = true    
        room_list_filter_1 = list(Room.objects.values('id', 'nombre', 'numero', 'descripcion', 'precio').filter(
            disponible=True, id_roomtype_id=int(json_get['tipo']), num_adultos__gte=int(json_get['select_num_adultos']), num_ninos__gte=int(json_get['select_num_ninos'])))
        print(room_list_filter_1)

        data = {
            'error': False,
            'data': room_list_filter_1,
        }        

        return JsonResponse(data)
    except:
        data = {
            'error': True,
            'message': 'Se ha producido un error en el requerimiento'
        }

        return JsonResponse(data)

    """ fechain = request.GET.get('fechain')
    fechaout = request.GET.get('fechaout')
    num = request.GET.get("tipo")
    adultos = request.GET.get("select_num_adultos")
    ninos = request.GET.get("select_num_ninos")
    room_list = []

    # Búsqueda de habitaciones solo disponibles

    out_queries = Room.objects.raw('''
               select r.id as id, r.precio as precio, rt.nombre as id_roomtype_id__nombre
                from reservas_room as r, reservas_roomtype as rt
                where r.id_roomtype_id=rt.id
                and disponible = true
                and num_adultos = 2
                and num_ninos = 1
                and id_roomtype_id = 1
                and r.id not in 
				(
                    select distinct b.room_id_id
                    from reservas_booking as b, reservas_bookingstate as bs, reservas_bookingtype as bt
                    where b.state_id_id = bs.id
                    and b.bookingtype_id_id = bt.id
                    and b.check_out_date > '2020-11-10'
                    and b.check_in_date < '2020-11-10') ''')
    for e in out_queries:
        room_list.append(e)
        print(e)

    print(room_list)
    return render(request, 'reservas/addreserva.html', {'habitaciones_disponibles': room_list}) """


def convert_date(string_date):
    dia = string_date.split('-')[2]
    mes = string_date.split('-')[1]
    ano = string_date.split('-')[0]

    return ano+'-'+mes+'-'+dia

###Administracion de reservas###


###Administracion de clientes###

def clientes(request):
    clientes_list = []
    out_queries = Perfil.objects.raw('''
        select ap.id, ap.name, ap.last_name, ap.cedula, ap.genero, au.email, ap.phone, ap.date_birth, au.is_removed
        from accesos_perfil as ap, accesos_usr as au
        where ap.usr_id_id = au.id
        and au.is_admin = false
        and au.is_staff = false
        and au.is_superuser=false;
    ''')

    for e in out_queries:
        if(e.cedula == None):
            e.phone = 'Sin dato'
        if(e.phone == None):
            e.phone = 'Sin dato'
        clientes_list.append(e)

    print(clientes_list)
    return render(request, 'clientes/clientes.html', {'clientes': clientes_list})

###Administracion de clientes###

class makeCheckInView(views.APIView):
    def post(self, request, pk):
        # Booking.bookings.get_object(pk = pk)
        bookingActual = get_object_or_404(Booking, pk=pk)
        print(Booking.objects)
        print("TEST")
        fecha_ingreso = datetime.datetime.now()
        #fecha_ingreso = datetime.datetime.now(timezone.utc)
        str_fecha_ingreso = fecha_ingreso.strftime("%Y-%m-%d %I:%M %p")
        bookingActual.fecha_ingresado = datetime.datetime.strptime(str_fecha_ingreso, '%Y-%m-%d %I:%M %p')
        bookingActual.save()
        respuesta = {'detail':  str_fecha_ingreso}
        return JsonResponse(respuesta)


class makeCheckOutView(views.APIView):
    def post(self, request, pk):
        # Booking.bookings.get_object(pk = pk)
        bookingActual = get_object_or_404(Booking, pk=pk)
        print(Booking.objects)
        print("TEST")
        fecha_salida = datetime.datetime.now()
        str_fecha_salida = fecha_salida.strftime("%Y-%m-%d %I:%M %p")        
        bookingActual.fecha_salida = datetime.datetime.strptime(str_fecha_salida, "%Y-%m-%d %I:%M %p")        
        bookingActual.save()
        respuesta = {'detail':  str_fecha_salida}
        return JsonResponse(respuesta)
        
class extenderReservaView(views.APIView):
    def post(self, request, pk, fecha ):
        # Booking.bookings.get_object(pk = pk)
       
        
        nuevafecha = fecha.split('.')[0]
        tmp = fecha.split('.')[1]
        print(tmp)
        tmp1 = tmp.split(':')[0]
        tmp2 = fecha.split(':')[1]
        fecha_sal = nuevafecha.split('-')[2]+"-"+nuevafecha.split('-')[1]+"-"+nuevafecha.split('-')[0]+" "+tmp1+":"+tmp2
        print(fecha_sal)
        bookingActual = get_object_or_404(Booking, pk=pk)
        


        fechasal_datetime = datetime.datetime.strptime(fecha_sal, '%Y-%m-%d %I:%M')      
        bookingActual.check_out_date = fechasal_datetime   
        fechain = bookingActual.check_out_date
        fechain = fechain.replace(tzinfo=None)
        fe = bookingActual.check_out_date
        fe = fe.replace(tzinfo=None)
        dif = fe -  fechain
        ##falta precio y noches
        bookingActual.no_nights=dif.days 
        print(bookingActual.no_nights)
        bookingActual.save()
        print(bookingActual.check_out_date)
        print(bookingActual.fecha_salida)
        respuesta = {'detail':  fechasal_datetime}
        return JsonResponse(respuesta)
####PAQUETES TURISTICOS####


class TourList(ListView):

    model = Tour_Package
    context_object_name = 'tours'
    template_name = 'tour-package/index_tours.html'


class TourCreate(CreateView):

    model = Tour_Package
    form_class = TourForm
    template_name = "tour-package/tour_create_form.html"

    success_url = reverse_lazy("administracion:tour_listar")


class TourEdit(UpdateView):

    model = Tour_Package
    context_object_name = 'tour'
    template_name = 'tour-package/tour_edit.html'
    form_class = TourForm

    def get_object(self):
        id_ = self.kwargs.get("id_tour")
        return get_object_or_404(Tour_Package, id=id_)

    success_url = reverse_lazy("administracion:tour_listar")


class TourEliminar(DeleteView):
    model = Tour_Package
    success_url = reverse_lazy("administracion:tour_listar")
    template_name = 'tour-package/tour_delete_form.html'

    def get_object(self):
        id_ = self.kwargs.get("id_tour")
        return get_object_or_404(Tour_Package, id=id_)


###ADMINISTRACION DE PUBLICIDAD NO INVASIVA

class PublicidadList(ListView):
    model = Publicidad
    context_object_name = 'anuncios'
    template_name = 'publicidad/publicidad_list.html'

class PublicidadCreate(CreateView):
    model = Publicidad
    form_class = PublicidadForm
    template_name = 'publicidad/publicidad_create_form.html'

    success_url = reverse_lazy('administracion:publicidad_listar')

class PublicidadEdit(UpdateView):

    model = Publicidad
    context_object_name = 'anuncio'
    template_name = 'publicidad/publicidad_edit.html'
    form_class = PublicidadForm

    def get_object(self):
        id_ = self.kwargs.get("id_anuncio")
        return get_object_or_404(Publicidad, id=id_)

    success_url = reverse_lazy("administracion:publicidad_listar")

class PublicidadDelete(DeleteView):
    model = Publicidad
    success_url = reverse_lazy("administracion:publicidad_listar")
    template_name = 'publicidad/publicidad_delete_form.html'

    def get_object(self):
        id_ = self.kwargs.get("id_anuncio")
        return get_object_or_404(Publicidad, id=id_)

def anuncio_test(request):
    anuncio = Publicidad.objects.filter(id=1).first()
    

##NOTICIAS
def noticia_create_form(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/administracion/noticias/index')
    else:
        form = NoticiaForm()
    return render(request, 'noticias/addNoticia.html', {
        'form': form
    })


class NoticiaCreate(CreateView):
    model = Noticia
    form_class = NoticiaForm
    template_name = "noticias/addNoticia.html"

    #success_url = reverse_lazy("administracion")
    success_url = reverse_lazy("/administracion/noticias/index")

class NoticiasList(ListView):
    model = Noticia
    context_object_name = 'noticias'
    template_name = 'noticias/listaNoticias.html'

class NoticiasEliminar(DeleteView):
    model = Noticia
    success_url = reverse_lazy("administracion:listaNoticias")
    template_name = 'noticias/noticias_delete_form.html'

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Noticia, id=id_)

class NoticiasEdit(UpdateView):

    model = Noticia
    context_object_name = 'noticias'
    template_name = 'noticias/noticias_edit.html'
    form_class = NoticiaForm

    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(Noticia, id=id_)

    success_url = reverse_lazy("administracion:listaNoticias")

###Administracion de checkout###

def checkouts_penalidad(request, booking_id):
    query_checkouts = Checkout.objects.raw('''
        select id, reason, details_reason, amount
        from reservas_checkout
        where booking_id_id = %s
        and is_canceled = %s
        and is_removed = %s
    ''', [int(booking_id), False, False])

    query_checkouts_canceled = Checkout.objects.raw('''
        select id, reason, details_reason, amount, details_canceled
        from reservas_checkout
        where booking_id_id = %s
        and is_canceled = %s
        and is_removed = %s
    ''', [int(booking_id), True, False])

    list_checkouts = []
    list_checkouts_canceled = []

    for e in query_checkouts:
        list_checkouts.append(e)

    for e in query_checkouts_canceled:
        list_checkouts_canceled.append(e)

    return render(request, 'checkouts/checkouts_administracion.html', {
        'list_checkouts': list_checkouts,
        'list_checkouts_canceled': list_checkouts_canceled,
        'booking_id': booking_id,
        'reason_checkout': REASON_CHECKOUT,
    })

def guardar_checkout_penalidad(request):
    if request.method=="POST":
        json_post = request.POST

        if(json_post['checkout_id']!=""):
            checkout_model = get_object_or_404(Checkout, id=json_post['checkout_id'])
            checkout_model.reason=json_post['reason']
            checkout_model.amount=json_post['amount']
            checkout_model.details_reason=json_post['details_reason']

            checkout_model.save()

        else:
            booking_model = get_object_or_404(Booking, id=json_post['booking_id'])

            checkout_model = Checkout(
                booking_id=booking_model,
                reason=json_post['reason'],
                details_reason=json_post['details_reason'],
                amount=json_post['amount'],
            )

            checkout_model.save()
                
        return redirect('/administracion/checkouts-penalidad/'+json_post['booking_id'])
    else:
        return redirect('/administracion/lista_reservas')

def eliminar_checkout_penalidad(request):
    if request.method=="POST":
        json_post = request.POST
        #print(json_post)
        checkout_model = get_object_or_404(Checkout, id=json_post['checkout_id_eliminacion'])
        checkout_model.is_canceled=True
        checkout_model.details_canceled=json_post['details_canceled']

        checkout_model.save()

        return redirect('/administracion/checkouts-penalidad/'+json_post['booking_id'])
    else:
        return redirect('/administracion/lista_reservas')

def reactivar_checkout_penalidad(request):
    if request.method=="POST":
        json_post = request.POST
        print(json_post)

        checkout_model = get_object_or_404(Checkout, id=json_post['checkout_id_reactivacion'])
        checkout_model.is_canceled=False
        checkout_model.details_canceled=""

        checkout_model.save()

        return redirect('/administracion/checkouts-penalidad/'+json_post['booking_id'])
    else:
        return redirect('/administracion/lista_reservas')

###Administracion de checkout###


def estadisticas(request):
    reservasList = list(Booking.objects.all().values('check_in_date', 'total_to_pay'))
    fechasList = []
    for reserva in reservasList:
        fechasList.append(reserva["check_in_date"].strftime("%d-%m-%Y"))
    print(reservasList[0]["check_in_date"].strftime("%d-%m-%Y"))
    return render(request, 'estadisticas/estadisticas.html', {'reservas': fechasList})

def chat(request):
    return render(request, 'chat/chat.html')

def suscripcion(request):
    if request.method=="POST":
        print("Envio masivo de promocion")
        json_post = request.POST
        print(json_post)                     

        subject = json_post['asunto']
        message = json_post['mensaje']
                
        email_from = settings.EMAIL_HOST_USER

        email_list = []
        out_queries = Perfil.objects.raw('''
            select au.id, au.email
            from accesos_usr as au
            where au.is_admin = false
            and au.is_staff = false
            and au.is_superuser=false;
        ''')

        for e in out_queries:            
            email_list.append(e.email)

        print(email_list)

        recipient_list = email_list
        send_mail(subject, message, email_from, recipient_list)

        return redirect('/administracion/suscripciones')

    else:
        clientes_list = []
        out_queries = Perfil.objects.raw('''
            select ap.id, ap.name, ap.last_name, ap.cedula, ap.genero, au.email, ap.phone, ap.date_birth, au.is_removed
            from accesos_perfil as ap, accesos_usr as au
            where ap.usr_id_id = au.id
            and au.is_admin = false
            and au.is_staff = false
            and au.is_superuser=false;
        ''')

        for e in out_queries:
            if(e.cedula == None):
                e.phone = 'Sin dato'
            if(e.phone == None):
                e.phone = 'Sin dato'
            clientes_list.append(e)

        print(clientes_list)
        return render(request, 'notificaciones/suscripcion.html', {'clientes': clientes_list})

def notificacion_reserva(request):
    if request.method=="POST":
        json_post = request.POST
        print(json_post)

        out_queries = Booking.objects.raw('''
            select au.id, au.email
            from reservas_booking as rb, accesos_perfil as ap, accesos_usr as au
            where rb.customer_id_id = ap.id and ap.usr_id_id = au.id and rb.id = %s
        ''', json_post['id_reserva'])

        email_list = []

        for e in out_queries:
            print(e)
            email_list.append(e.email)

        print(email_list)

        subject = json_post['asunto']
        message = json_post['mensaje']
                
        email_from = settings.EMAIL_HOST_USER

        recipient_list = email_list
        send_mail(subject, message, email_from, recipient_list)

        return redirect('/administracion/notificacion-reserva')

    else:
        print("Entraaaaa a listar")
        reservas_list = []
        out_queries = Booking.objects.raw('''
            select b.id, b.check_in_date, b.check_out_date, p.name, p.last_name, p.cedula, r.nombre, r.numero
            from reservas_booking as b, accesos_perfil as p, reservas_room as r
            where b.customer_id_id = p.id and b.room_id_id = r.id
        ''')
        print(out_queries)
        for e in out_queries:
            print(e)
            reservas_list.append(e)
            e.check_in_date = e.check_in_date.strftime("%Y-%m-%d %I:%M %p")
            e.check_out_date = e.check_out_date.strftime("%Y-%m-%d %I:%M %p")
            if(e.fecha_ingresado is None):
                e.fecha_ingresado = "-"
            else:
                e.fecha_ingresado = e.fecha_ingresado.strftime("%Y-%m-%d %I:%M %p")
            if(e.fecha_salida is None):
                e.fecha_salida = "-"
            else:
                e.fecha_salida = e.fecha_salida.strftime("%Y-%m-%d %I:%M %p")

        return render(request, 'notificaciones/notificacion_reserva.html', {'lista_reservas': reservas_list})