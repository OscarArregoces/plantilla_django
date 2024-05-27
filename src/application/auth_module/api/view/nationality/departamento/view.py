from responses import Response
from src.application.auth_module.api.serializers.nationality.departamento_serializer import DepartamentoSerializer
from src.application.auth_module.models import Departamento
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from configs.helpers.PaginationView import DecoratorPaginateView

class DepartamentosView(APIView):
    # @DecoratorPaginateView
    def get(self, request, *args, **kwargs):
        try:
            departamentos = Departamento.objects.all() 
            departamentos_serializer = DepartamentoSerializer(departamentos, many=True)
            return Response(departamentos_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
class DepartamentosByPaisView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            pais_id = kwargs.get("pais_id", None)
            if(pais_id):
                departamentos = Departamento.objects.filter(pais_id=pais_id)
                departamentos_serializer = DepartamentoSerializer(departamentos, many=True)
                return Response(departamentos_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"error":"id de pais es requerido"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        