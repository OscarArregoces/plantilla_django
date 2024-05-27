from rest_framework import serializers
from src.application.auth_module.api.serializers.nationality.pais_serializer import PaisSerializer

from src.application.auth_module.models import Departamento

class DepartamentoSerializer(serializers.ModelSerializer):
    # pais = PaisSerializer(read_only=True)
    class Meta:
        model = Departamento
        exclude= ("createdAt","updateAt","userCreate","userUpdate","visible")
