from rest_framework import serializers

from src.application.auth_module.models import Pais

class PaisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pais
        exclude= ("createdAt","updateAt","userCreate","userUpdate","visible")
