from django.urls import include, path

from . import views

app_name = 'accesos'

urlpatterns = [
    path('login', views.login_cliente, name ='login'),
    path('registro', views.registro),
    path('login_social', views.login_social),
    path('registro_social', views.registro_social),
    path('profile', views.my_profile, name='profile'),
    path('profile/edit/',views.ProfileEdit.as_view(),name='edit_profile'),
    path('recuperar-contraseña', views.recuperar_contrasena),
    path('nueva-contraseña', views.nueva_contrasena),
]