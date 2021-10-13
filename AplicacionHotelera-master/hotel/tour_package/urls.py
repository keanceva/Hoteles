from django.urls import path
from . import views

app_name = 'tour_package'

urlpatterns = [
    path('',views.TourList.as_view(),name='list_tours'),
    path('<int:pk>',views.ParticularOrder.as_view(), name = "detail_view"),
]