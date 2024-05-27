from rest_framework import serializers
from src.application.auth_module.api.serializers.nationality.departamento_serializer import DepartamentoSerializer

from src.application.auth_module.models import Ciudad

class CiuadadSerializer(serializers.ModelSerializer):
    # departamento = DepartamentoSerializer(read_only=True)
    class Meta:
        model = Ciudad
        exclude= ("createdAt","updateAt","userCreate","userUpdate","visible")
