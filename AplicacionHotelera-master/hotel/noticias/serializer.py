from rest_framework import serializers
from .models import Noticia

class NoticiaSerialiser(serializers.HyperlinkedModelSerializer):
    path_image = serializers.ImageField(
            max_length = None, use_url=True
        )  
    class Meta:
        model = Noticia
        fields = ('id', 'titulo', 'noticia', 'path_image', 'create_date', 'update_date')