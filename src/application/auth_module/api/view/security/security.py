from rest_framework.views import APIView
from rest_framework import status

from src.application.auth_module.api.serializers.resources.resources_serializers import ResourcesRolesSerializers, ResourcesSerializers, SecurityRolesResourceSerializer
from ....models import Resources, Resources_roles, User
from rest_framework.response import Response
from django.contrib.auth.models import Group

class SecurityRolesPerson(APIView):
    def put(self, request, *args, **kwargs):
        
        person_id = request.data.get('person_id')
        roles_id = request.data["roles"]
        
        if person_id is None or roles_id is None:
            return Response({'error': 'person_id and roles are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.get(person_id=person_id)
        
        roles = Group.objects.filter(id__in=roles_id)

        try:
            if roles:
                User.objects.get(pk=user.id).groups.set([x.pk for x in roles])   #type: ignore
                return Response({'message': 'Roles updated successfully'}, status.HTTP_200_OK)
        except Exception as e:
            return Response(e.args, status.HTTP_400_BAD_REQUEST)
        
        
class SecurityRolesResource(APIView):
    
    def get(self, request, *args, **kwargs):
        
            rol_id = kwargs.get("rol_id",None)
            if rol_id is None:
                return Response({"error": "rol_id es requerido."}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                role = Group.objects.get(id=rol_id)
            except Group.DoesNotExist:
                return Response({"error": "El rol especificado no existe."}, status=status.HTTP_404_NOT_FOUND)

            resources_roles = Resources_roles.objects.filter(rolesId=role)
            serializer = SecurityRolesResourceSerializer(resources_roles, many=True)

            response_data = {
                'role_name': role.name,  # Asegúrate de tener este campo en tu modelo Group
                'resources': serializer.data
            }

            return Response(response_data, status=status.HTTP_200_OK)
        
    def put(self, request, *args, **kwargs):
        role_id = request.data.get("role_id",None)
        resource_ids = request.data.get("resource_ids", None)
        
        if role_id is None or resource_ids is None:
            return Response({"error": "role_id and resource_ids are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        
        try:
            role = Group.objects.get(id=role_id)
        except Group.DoesNotExist:
            return Response({"error": "El rol especificado no existe."}, status=status.HTTP_404_NOT_FOUND)

        
        existing_resources = Resources_roles.objects.filter(rolesId=role)

        existing_resource_ids = set(existing_resource.resourcesId.id for existing_resource in existing_resources)  #type: ignore

        new_resource_ids = set(resource_ids)

        resources_to_delete = existing_resource_ids - new_resource_ids

        resources_to_create = new_resource_ids - existing_resource_ids

        Resources_roles.objects.filter(rolesId=role, resourcesId__in=resources_to_delete).delete()

        for resource_id in resources_to_create:
            resource = Resources.objects.get(id=resource_id)
            Resources_roles.objects.create(resourcesId=resource, rolesId=role)

        return Response({"message": "Recursos actualizados correctamente para el rol."}, status=status.HTTP_200_OK)


