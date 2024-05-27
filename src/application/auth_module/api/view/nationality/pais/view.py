from responses import Response
from src.application.auth_module.models import Pais
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from src.application.auth_module.api.serializers.nationality.pais_serializer import PaisSerializer
from configs.helpers.PaginationView import DecoratorPaginateView

class PaisesView(APIView):
    # @DecoratorPaginateView
    def get(self, request, *args, **kwargs):
        try:
            paises = Pais.objects.all() 
            paises_serializer = PaisSerializer(paises, many=True)
            # return paises_serializer.data
            return Response(paises_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        