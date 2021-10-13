from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.conf import settings
from django.core.mail import send_mail

# Modelos
from accesos.models import Usr
from accesos.models import Perfil

#Formularios
from accesos.forms import ProfileForm

# Create your views here.
@csrf_protect
def login_cliente(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email is None or password is None:
            # return HttpResponse("Por favor ingrese el email y contrasena!")
            request.session['success_login'] = False
            return redirect('/accesos/login')
        try:
            usr = Usr.objects.get(email=email)
            # print(password)
            # print(usr.password)
            if(check_password(password, usr.password)):
                perfil = Perfil.objects.get(usr_id_id=usr.id)
                if 'success_register' in request.session:
                    del request.session['success_register']
                    
                if 'success_change' in request.session:
                    del request.session['success_change']

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

                return redirect('/reservas')
            else:
                print("entra a false")
                request.session['success_login'] = False
                return redirect('/accesos/login')

        except Exception as error:
            print(error)
            request.session['success_login'] = False
            return redirect('/accesos/login')
    else:
        return render(request, 'login_cliente.html')


@csrf_protect
def registro(request):
    if 'success_login' in request.session:
        del request.session['success_login']
        
    if request.method == 'POST':
        try:
            nombres = request.POST.get('nombres')
            apellidos = request.POST.get('apellidos')
            fecha_nacimiento = request.POST.get('fecha_nacimiento')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password_hash = make_password(password)
            print(password)
            print(password_hash)

            usr = Usr(
                username=email.split('@')[0],
                email=email,
                password=password_hash,
                is_admin=False
            )

            usr.save()

            perfil = Perfil(
                usr_id=usr,
                name=nombres,
                last_name=apellidos,
                date_birth=fecha_nacimiento,
            )

            perfil.save()

            request.session['success_register'] = True
            if 'success_change' in request.session:
                del request.session['success_change']
            return redirect('/accesos/login')

        except Exception as error:
            print(error)
            request.session['success_register'] = False
            return redirect('/accesos/login')
    else:
        return render(request, 'registro_form.html')


def login_social(request):
    try:
        usr = Usr.objects.get(id=request.user.id)

        perfil = Perfil.objects.get(usr_id_id=usr.id)

        if 'success_register' in request.session:
            del request.session['success_register']

        if 'success_change' in request.session:            
            del request.session['success_change']
        
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

        return redirect('/reservas')

    except Exception as error:
        print(error)
        request.session['success_register'] = False
        return redirect('/accesos/login')


@csrf_protect
def registro_social(request):
    if 'success_login' in request.session:
        del request.session['success_login']

    if request.method == 'POST':
        try:
            usr = Usr.objects.get(id=request.user.id)

            perfil = Perfil(
                usr_id=usr,
                name=request.POST.get('nombres'),
                last_name=request.POST.get('apellidos'),
                date_birth=request.POST.get('fecha_nacimiento'),
            )

            perfil.save()

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

            if 'success_change' in request.session:
                del request.session['success_change']

            return redirect('/reservas')
        except Exception as error:
            print(error)
            request.session['success_register'] = False
            return redirect('/accesos/login')
    else:
        try:
            usr = Usr.objects.get(id=request.user.id)

            if 'success_register' in request.session:
                del request.session['success_register']
            request.session['success_login'] = True
            request.session.modified = True

            customer_json = {
                'email': usr.email,
                'username': usr.username
            }

            print(customer_json)
            request.session['customer'] = customer_json

            return render(request, 'registro_social.html')

        except Exception as error:
            print(error)
            request.session['success_register'] = False
            return redirect('/accesos/login')


def my_profile(request):
    perfil = Perfil.objects.filter(id=request.session['customer']['customer_id']).first()
    #user = Usr.objects.filter(id=perfil.usr_id_id)

    return render(request,'profile.html', {'user':perfil})
    
class ProfileEdit(UpdateView):

    model = Perfil
    context_object_name = 'perfil'
    template_name = 'profile/profile_edit.html'
    form_class = ProfileForm

    def get_object(self):
        id_perfil = self.request.session['customer']['customer_id']
        return get_object_or_404(Perfil,id=id_perfil)

    success_url = reverse_lazy("accesos:profile")

def recuperar_contrasena(request):

    if 'success_login' in request.session:
        del request.session['success_login']

    if request.method=="POST":        
        json_post = request.POST             

        subject = "RECUPERACIÓN DE CONTRASEÑA"
        message = """
        Buenas tardes,

        Para recuperar su contraseña, por favor acceder al siguiente enlace e ingresar nueva contraseña.
        http://localhost:8000/accesos/nueva-contraseña
        """
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [json_post['email'], ]
        send_mail(subject, message, email_from, recipient_list)

        return redirect('/accesos/recuperar-contraseña')
    else:
        return render(request, 'recuperar_contrasena.html')

def nueva_contrasena(request):

    if 'success_login' in request.session:
        del request.session['success_login']

    if request.method=="POST":
        json_post = request.POST
        print(json_post)

        email_test = "emiliojmp9@gmail.com"

        password_hash = make_password(json_post['password'])

        usr = Usr.objects.get(email=email_test)
        usr.password = password_hash

        usr.save()

        request.session['success_change'] = True        

        return redirect('/accesos/login')
    else:
        return render(request, 'nueva_contrasena.html')