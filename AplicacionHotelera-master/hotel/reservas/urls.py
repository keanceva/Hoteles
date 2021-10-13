from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'reservas'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('test/',views.test,name='test'),
    path('busqueda-normal', views.busqueda_normal),
    path('paquetes_turisticos', views.show_packages),
    path('rooms<int:profile_id>',views.rooms, name="list_bookings"),
    path('habitacion-detalles/<int:id>', views.show_details_room),
    path('add-to-cart/<int:id_cuarto>',views.add_to_cart, name="add-to-cart"), 
    path('historial/',views.BookingRecords.as_view(),name= "historial-reservas"),   
]