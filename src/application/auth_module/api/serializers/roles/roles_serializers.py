from ....models import User
from rest_framework import serializers
from django.contrib.auth.models import Group


class GroupSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
            
class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"

class GroupPayloadValidateSerializer(serializers.Serializer):
    name = serializers.CharField()
    def validate(self, data):
        for campo in ['name']:
            if campo not in data:
                raise serializers.ValidationError(f"El campo '{campo}' es requerido")
        
        for campo in ['name']:
            if not isinstance(data[campo], str):
                raise serializers.ValidationError(f"El campo '{campo}' debe ser una string")

        return data
    

