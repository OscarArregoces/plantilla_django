from ....models import Document_types
from rest_framework import serializers

class DocumentSerializersView(serializers.Serializer):
    id = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        fields = '__all__'

class DocumentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Document_types
        fields = '__all__'
