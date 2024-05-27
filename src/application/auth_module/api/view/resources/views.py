from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from src.application.auth_module.api.serializers.resources.resources_serializers import ResourcesCreateSerializers, ResourcesPayloadValidateSerializer, ResourcesSerializers
from ....models import Resources

class ResourcesView(APIView):
    
    def get (self, request, *args, **kwargs):
        try:
            resources = Resources.objects.all();
            resources_serializer = ResourcesSerializers(resources, many=True)
            return Response(resources_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
    
    def post (self, request, *args, **kwargs):
        ResourcesPayloadValidateSerializer().validate(request.data)
        try:
            serializer = ResourcesCreateSerializers(data=request.data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    return Response({"message": "Recursos creados exitosamente"}, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except  Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
    
    
    def put (self, request, *args, **kwargs):
        recurso_id = kwargs.get("recurso_id",None)
        if recurso_id is None:
            return Response({"error":"recurso_id es requerido"},status=status.HTTP_400_BAD_REQUEST)
        try:
            resource = Resources.objects.get(id=recurso_id)
            if resource is None:
                return Response({"error":"recurso no encontrado"},status=status.HTTP_404_NOT_FOUND)
            
            serializer = ResourcesCreateSerializers(resource, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Recurso actualizado exitosamente"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except  Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
    def delete (self, request, *args, **kwargs):
        recurso_id = kwargs.get("recurso_id",None)
        if recurso_id is None:
            return Response({"error":"recurso_id es requerido"},status=status.HTTP_400_BAD_REQUEST)
        try:
            resource = Resources.objects.get(id=recurso_id)
            if resource is None:
                return Response({"error":"recurso no encontrado"},status=status.HTTP_404_NOT_FOUND)
            
            resource.delete()
            return Response({"message": "Recurso eliminado exitosamente"}, status=status.HTTP_200_OK)
        except  Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
        