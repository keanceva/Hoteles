from django.urls import path

from .views import CardTokenView


urlpatterns = [
    path('cardToken/', CardTokenView.as_view(), name="card-token")
]