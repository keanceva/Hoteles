from django.urls import path

from . import views

app_name = "shopping-cart"

urlpatterns = [
    path('', views.list_cart,name="list_cart"),
]