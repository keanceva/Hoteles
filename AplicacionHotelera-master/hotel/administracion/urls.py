from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

app_name = 'administracion'

urlpatterns = [
    path('', views.index),
    path('rooms',views.RoomList.as_view(), name="room_list"),
    path('rooms/create',views.room_create_form, name="room_create"),
    path('rooms/editar/<int:id_room>/',views.RoomEdit.as_view(),name = 'room_edit'),
    path('rooms/eliminar/<int:id_room>/',views.RoomDelete.as_view(),name = 'room_delete'),
    path('rooms/test/',views.upload_image_room),
    path('login', views.login),
    path('logout', views.logout_admin),
    path('administradores', views.administradores),

    path('form', views.model_form_upload, name='model_form_upload'),



    path('lista_reservas/', views.lista_reservas),
    path('buscarcliente/', views.buscarcliente),
    path('eliminar_reserva/<int:id>', views.eliminar_reserva),
    path('agregar_reserva', views.agregar_reserva),
    path('reservas', views.reservas),    
    path('buscarhabitaciones/', views.buscarhabitaciones),


    path('administrador-eliminacion/<int:id>', views.administrador_eliminacion),
    path('administrador-edicion/<int:id>', views.administrador_edicion),
    path('administrador-nuevo', views.administrador_nuevo),
    

    path('tours',views.TourList.as_view(), name="tour_listar"),
    path('tours/crear/',views.TourCreate.as_view(),name = 'tour_crear'),
	path('tours/editar/<int:id_tour>/',views.TourEdit.as_view(),name = 'tour_editar'),
	path('tours/eliminar/<int:id_tour>/', views.TourEliminar.as_view(), name = 'tour_eliminar'),

    path('publicidad/',views.PublicidadList.as_view(),name="publicidad_listar"),
    path('publicidad/crear',views.PublicidadCreate.as_view(),name="publicidad_crear"),
    path('publicidad/editar/<int:id_anuncio>/',views.PublicidadEdit.as_view(),name="publicidad_editar"),
    path('publicidad/eliminar/<int:id_anuncio>/',views.PublicidadDelete.as_view(),name="publicidad_eliminar"), 



    ###Habitaciones disponibles###
    path('habitaciones-disponibles', views.habitaciones_disponibilidad),
    ###Habitaciones disponibles###
    path('clientes', views.clientes),
    #path('makeCheckIn/<pk>/', views.makeCheckIn, name="hacer_checkin"),
    path('makeCheckIn/<pk>/', views.makeCheckInView.as_view(), name="hacer_checkin"),
    path('makeCheckOut/<pk>/', views.makeCheckOutView.as_view(), name="hacer_checkout"),
    path('extenderReserva/<pk>/<str:fecha>/', views.extenderReservaView.as_view(), name="hacer_extension"),

    path('noticias/create',views.noticia_create_form, name="noticia_create"),
    path('noticias/index',views.NoticiasList.as_view(), name="listaNoticias"),
	path('noticias/eliminar/<int:id>/', views.NoticiasEliminar.as_view(), name = 'noticia_eliminar'), 
    path('noticias/editar/<int:id>/',views.NoticiasEdit.as_view(),name = 'noticia_editar'),

    #Checkouts
    path('checkouts-penalidad/<int:booking_id>', views.checkouts_penalidad),
    path('guardar-checkout-penalidad', views.guardar_checkout_penalidad),
    path('eliminar-checkout-penalidad', views.eliminar_checkout_penalidad),

    path('reactivar-checkout-penalidad', views.reactivar_checkout_penalidad),


    path('reactivar-checkout-penalidad', views.reactivar_checkout_penalidad),   

    #estadisticas
    path('estadisticas', views.estadisticas),

    path('chat', views.chat),

    #Notificaciones#
    path('suscripciones', views.suscripcion),
    path('notificacion-reserva', views.notificacion_reserva),
    ]    