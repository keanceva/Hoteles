from rest_framework import serializers
from .models import Booking


class BookingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking

        