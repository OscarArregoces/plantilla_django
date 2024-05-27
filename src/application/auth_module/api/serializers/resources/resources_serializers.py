from ....models import Resources, Resources_roles
from rest_framework.serializers import (
    Serializer,
    IntegerField,
    BooleanField,
    CharField,
    ListField,
    ValidationError,
    ModelSerializer
)

class ResourcesSerializers(Serializer):
    id = IntegerField(read_only=True)
    path = CharField(read_only=True)
    id_padre = IntegerField(read_only=True)
    icono = CharField(read_only=True)
    link = CharField(read_only=True)
    titulo = CharField(read_only=True)

class SecurityRolesResourceSerializer(ModelSerializer):
    # id = IntegerField(read_only=True)
    # resourcesId = IntegerField(read_only=True)
    class Meta:
        model = Resources_roles
        fields = '__all__'
        
class ResourcesCreateSerializers(Serializer):
    herencia = BooleanField()
    resources = ListField()
    
    def create(self, validated_data):
        try:
            herencia = validated_data.get('herencia')
            resources_data = validated_data.get('resources')
            
            if herencia:
                resource_data = resources_data[0]
                path = resource_data.get("path", None)
                id_padre = resource_data.get("id_padre", 0)
                link = resource_data.get("link", None)
                titulo = resource_data.get("titulo", None)
                icono = resource_data.get("icono", "icono")

                if path is not None:  # Validar que path no sea nulo
                    return Resources.objects.create(
                        pk=Resources.objects.last().pk + 1,   #type: ignore  
                        path=path,
                        id_padre=id_padre,
                        link=link,
                        titulo=titulo,
                        method="GET",
                        icono=icono,
                    )
                else:
                    raise ValidationError("El campo 'path' no puede ser nulo")
            else:
                parent_id = 0
                for resource_data in resources_data:
                    path = resource_data.get("path", None)
                    link = resource_data.get("link", None)
                    titulo = resource_data.get("titulo", None)
                    icono = resource_data.get("icono", "icono")

                    if path is not None:  # Validar que path no sea nulo
                        instance = Resources.objects.create(
                            pk=Resources.objects.last().pk + 1,   #type: ignore  
                            path=path,
                            id_padre=parent_id,
                            link=link,
                            titulo=titulo,
                            method="GET",
                            icono=icono,
                        )
                        parent_id = instance.pk
                    else:
                        raise ValidationError("El campo 'path' no puede ser nulo")
                return instance
        except Exception as e:
            raise e
    def update(self, instance, validated_data):
        try:
            resources_data = validated_data.get('resources')
            resource_data = resources_data[0]
            
            path = resource_data.get("path", None)
            id_padre = resource_data.get("id_padre", 0)
            link = resource_data.get("link", None)
            titulo = resource_data.get("titulo", None)
            icono = resource_data.get("icono", "icono")

            instance.path = path
            instance.id_padre = id_padre
            instance.link = link
            instance.titulo = titulo
            instance.icono = icono
            instance.save()
                        
            return instance
        except Exception as e:
            raise e


class ResourcesPayloadValidateSerializer(Serializer):
    herencia = BooleanField()
    resources = ResourcesSerializers(many=True)

    def validate(self, data):
        for campo in ['herencia', 'resources']:
            if campo not in data:
                raise ValidationError(f"El campo '{campo}' es requerido")
            
        if not isinstance(data['resources'], list):
            raise ValidationError("El campo 'resources' debe ser una lista")

        if not isinstance(data['herencia'], bool):
            raise ValidationError("El campo 'herencia' debe ser un booleano")
  
        return data

class ResourcesRolesSerializers(Serializer):
    merge = BooleanField(required=False)
    rolesId = IntegerField()
    resources = ListField(child=IntegerField())

    def create(self, validated_data):
        try:
            
            print(validated_data)
            
            list_resources_roles = [
                Resources_roles(
                    rolesId_id=validated_data["rolesId"], resourcesId_id=resource
                )
                for resource in validated_data.get("resources", [])
            ]

            instane = Resources_roles.objects.bulk_create(list_resources_roles)[0]
            return instane
        except Exception as e:
            raise e
