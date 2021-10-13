from rest_framework import generics
from rest_framework import views
from rest_framework.response import Response
from .CardToken import CardToken
from .serializers import CardTokenSerializer


class CardTokenView(views.APIView):
    """
    Provides a get method handler.
    """
    def get(self, request):
        cardToken = CardToken()
        results = CardTokenSerializer(cardToken).data
        return Response(results)