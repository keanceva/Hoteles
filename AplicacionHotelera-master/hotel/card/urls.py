from django.urls import path

from . import views

app_name = "card"
urlpatterns = [
    path('addCard', views.index),
    path('showCards', views.showCards),
]