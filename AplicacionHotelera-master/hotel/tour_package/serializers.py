from .models import Tour_Package
from rest_framework import serializers

class TourSerializer(serializers.HyperlinkedModelSerializer):

	class Meta:
		model = Tour_Package
		fields = ['title','description','available_stock','company','days','hours','price','path_image']