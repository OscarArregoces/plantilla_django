from rest_framework import serializers
from src.application.auth_module.api.serializers.academico.tipoPrograma_serializers import TipoProgramaSerializer
from src.application.auth_module.models import Headquarters, Faculties, Programs


class BaseSerializers(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    createdAt = serializers.DateField(read_only=True)
    updateAt = serializers.DateField(read_only=True)
    userCreate = serializers.SlugRelatedField("username", read_only=True)
    userUpdate = serializers.SlugRelatedField("username", read_only=True)

    def __init__(self, instance=None, data=..., **kwargs):
        meta = bool(kwargs.pop("meta", None))

        super().__init__(instance, data, **kwargs)

        if meta != True or meta is None:
            self.fields.pop("createdAt")
            self.fields.pop("updateAt")
            self.fields.pop("userCreate")
            self.fields.pop("userUpdate")


class HeadSerializers(BaseSerializers):
    name = serializers.CharField()

    class Meta:
        fields = "__all__"

    def create(self, validated_data):
        head = Headquarters.objects.create(name=validated_data["name"])
        return head

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance


class FacultiesSerializersView(BaseSerializers):
    name = serializers.CharField(read_only=True)

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "name": instance.name,
            # "sede": {"id": instance.headquarter.id, "name": instance.headquarter.name},
        }

    class Meta:
        fields = "__all__"


class FacultiesSerializers(BaseSerializers):
    name = serializers.CharField()
    class Meta:
        fields = "__all__"

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "name": instance.name,
        }

    def create(self, validated_data):
        faculties = Faculties.objects.create(
            name=validated_data["name"]
        )
        return faculties

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance


class ProgramsSerializersView(BaseSerializers):
    name = serializers.CharField(read_only=True)
    facultad = FacultiesSerializers(read_only=True)
    tipo_programa = TipoProgramaSerializer(read_only=True)

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "name": instance.name,
            "facultad": {"id": instance.facultad.id, "name": instance.facultad.name},
            "tipo_programa": {"id": instance.tipo_programa.id, "name": instance.tipo_programa.name},
        }

    class Meta:
        fields = "__all__"


class ProgramsSerializers(BaseSerializers):
    name = serializers.CharField()
    # facultad = FacultiesSerializers(read_only=True)
    # tipo_programa = TipoProgramaSerializer(read_only=True)
    facultad = serializers.IntegerField()
    tipo_programa = serializers.IntegerField()

    class Meta:
        fields = "__all__"

    def create(self, validated_data):
        program = Programs.objects.create(
            name=validated_data["name"],
            facultad_id=validated_data["facultad"],
            tipo_programa_id=validated_data["tipo_programa"]
        )
        return program

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.facultad_id = validated_data.get("facultad", instance.facultad)
        instance.tipo_programa_id = validated_data.get("tipo_programa", instance.tipo_programa)
        instance.save()
        return instance
