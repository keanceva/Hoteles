from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'noticias', views.NoticiasViewSet)
router.register(r'tours',views.ToursViewSet)

urlpatterns = [
    path('login', views.login),
    path('register', views.registro),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]