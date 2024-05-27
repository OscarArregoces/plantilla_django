from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import Group

from src.application.auth_module.api.serializers.roles.roles_serializers import GroupCreateSerializer, GroupPayloadValidateSerializer, GroupSerializer

class RolesView(APIView):
    
  def get (self, request, *args, **kwargs):
        try:
            groups = Group.objects.all()
            groups_serializer = GroupSerializer(groups, many=True)
            return Response(groups_serializer.data, status=status.HTTP_200_OK)
        except  Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
  def post (self, request, *args, **kwargs):
        GroupPayloadValidateSerializer().validate(request.data)
        try:
            serializer = GroupCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Rol creado exitosamente"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except  Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
  def put (self, request, *args, **kwargs):
        rol_id = kwargs.get("rol_id",None)
        
        if rol_id is None:
            return Response({"error":"rol_id es requerido"},status=status.HTTP_400_BAD_REQUEST)
        
        GroupPayloadValidateSerializer().validate(request.data)
        try:
            rol = Group.objects.get(id=rol_id)
            serializer = GroupCreateSerializer(rol, data=request.data, partial=True)
            
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Rol actualizado exitosamente"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except  Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        