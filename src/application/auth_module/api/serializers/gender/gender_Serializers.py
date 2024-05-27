from rest_framework import serializers
from ....models import Genders


class GenderSerializersView(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        fields = "__all__"


class GenderSerializers(serializers.Serializer):
    name = serializers.CharField()

    class Meta:
        fields = "__all__"

    def create(self, validated_data):
        try:
            gender = Genders.objects.create(name=validated_data["name"])

            return gender
        except Exception as e:
            raise serializers.ValidationError(e.args, 404)

    def update(self, instance, validated_data):
        instance.name = validated_data.pop("name", instance.name)
        instance.save()
        return instance
