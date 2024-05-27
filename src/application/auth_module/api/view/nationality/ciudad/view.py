from responses import Response
from src.application.auth_module.api.serializers.nationality.ciudad_serializer import CiuadadSerializer
from src.application.auth_module.api.serializers.nationality.departamento_serializer import DepartamentoSerializer
from src.application.auth_module.models import Ciudad
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from configs.helpers.PaginationView import DecoratorPaginateView

class CiudadesView(APIView):
    # @DecoratorPaginateView
    def get(self, request, *args, **kwargs):
        try:
            ciudades = Ciudad.objects.all() 
            ciudades_serializer = CiuadadSerializer(ciudades, many=True)
            # return paises_serializer.data
            return Response(ciudades_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

class CiudadesByDepartamentoView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            departamento_id = kwargs.get("departamento_id", None)
            if(departamento_id):
                ciudades = Ciudad.objects.filter(departamento_id=departamento_id)
                ciudades_serializer = CiuadadSerializer(ciudades, many=True)
                return Response(ciudades_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error":"id de pais es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
class CiudadesByPais(APIView):
    def get(self, request, *args, **kwargs):
        try:
            pais_id = kwargs.get("pais_id", None)
            if(pais_id):
                ciudades = Ciudad.objects.filter(pais_id=pais_id)
                ciudades_serializer = CiuadadSerializer(ciudades, many=True)
                return Response(ciudades_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error":"id de pais es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        