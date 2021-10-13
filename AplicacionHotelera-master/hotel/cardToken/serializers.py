from rest_framework import serializers

class CardTokenSerializer(serializers.Serializer):
    cardToken = serializers.CharField(max_length=255)