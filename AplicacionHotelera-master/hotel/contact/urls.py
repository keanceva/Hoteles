from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'contact'

urlpatterns = [
    path('', views.contact, name = 'contact'),
    path('send-email', views.send_email, name = 'send_email'),
    path('to-suscribe', views.to_suscribe, name = 'to_suscribe'),
]