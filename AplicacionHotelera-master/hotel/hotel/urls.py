"""hotel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accesos/', include('accesos.urls')),
    path('reservas/', include('reservas.urls')),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('shopping-cart/', include('shopping_cart.urls')),
    path('card/', include('card.urls')),
    path('cardToken/', include('cardToken.urls')),
    path('tours/', include('tour_package.urls')),
    re_path('api/', include('cardToken.urls')),
    path('api_mobile/', include('api_mobile.urls')),
    path('administracion/', include('administracion.urls')),
    path('noticias/', include('noticias.urls')),
    path('contact/', include('contact.urls')),
    path('chat/', include('chat.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
