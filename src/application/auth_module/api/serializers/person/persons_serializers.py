from src.application.auth_module.api.serializers.nationality.ciudad_serializer import CiuadadSerializer
from src.application.auth_module.api.serializers.nationality.departamento_serializer import DepartamentoSerializer

from src.application.auth_module.api.serializers.nationality.pais_serializer import PaisSerializer
from ....models import Document_types, Genders, Persons
from rest_framework.serializers import (
    ModelSerializer,
    Serializer,
    CharField,
    EmailField,
    DateField,
    IntegerField,
    BooleanField,
    PrimaryKeyRelatedField,
)
from ..document.document_serializers import DocumentSerializersView
from ..gender.gender_Serializers import GenderSerializersView
from rest_framework.validators import UniqueValidator


class PersonsSerializers(Serializer):
    document_type = DocumentSerializersView(required=False)
    gender_type = GenderSerializersView(required=False)
    address = CharField(required=False)
    nationality = CharField(required=False)
    date_of_birth = CharField(required=False)
    phone2 = CharField(required=False)
    email2 = CharField(required=False, allow_blank=True)
    document_type = IntegerField(required=False)
    gender_type = IntegerField(required=False)

    class Meta:
        model = Persons
        exclude = ("createdAt", "updateAt", "visible", "userCreate", "userUpdate", "status","name")
    
    def create(self, validated_data,):
        document_type_id = validated_data.pop('document_type', None)
        gender_type_id = validated_data.pop('gender_type', None)

        if document_type_id:
            validated_data['document_type'] = Document_types.objects.get(pk=document_type_id)

        if gender_type_id:
            validated_data['gender_type'] = Genders.objects.get(pk=gender_type_id)
            
        
        return Persons.objects.create(**{**validated_data, 'email2':None,})
    
class PersonsCreateSerializer(ModelSerializer):
    class Meta:
        model = Persons
        fields = '__all__'
        
class PersonsCreatePartialSerializer(Serializer):
    phone = CharField(allow_blank=False)
    phone2 = CharField(required=False, allow_blank=True)
    email = CharField(allow_blank=False)
    email2 = CharField(required=False, allow_blank=True)
    
    def update(self, instance, validated_data):
        try:
            instance.phone = validated_data.get("phone", instance.phone)
            instance.phone2 = validated_data.get("phone2", instance.phone2)
            instance.email = validated_data.get("email", instance.email)
            instance.email2 = validated_data.get("email2", instance.email2)
            instance.save()
                        
            return instance
        except Exception as e:
            raise e

class PersonsDetailSerializers(ModelSerializer):
    nationality = PaisSerializer(read_only=True)
    departamento = DepartamentoSerializer(read_only=True)
    municipio = CiuadadSerializer(read_only=True)
    document_type= DocumentSerializersView(read_only=True)
    gender_type = GenderSerializersView(read_only=True)
    class Meta:
        model = Persons
        exclude = ("createdAt", "updateAt", "visible", "userCreate", "userUpdate", "status","name")
    
class PersonsSimpleSerializersView(Serializer):
    id = IntegerField(read_only=True)
    nationality = PaisSerializer(read_only=True)
    fullname = CharField(read_only=True)
    identification = CharField(read_only=True)
    email = EmailField(read_only=True)
    
    # class Meta:
    #     model = Persons
    #     fields = ('id','fullname','nationality','identification',)

class UserEventoSerializer(ModelSerializer):
    
    class Meta:
        model = Persons
        fields = ('id','fullname','email','phone', 'graduado', 'funcionario')
        read_only_fields = fields

queryset = Persons.objects.all()

class PersonsSerializer(Serializer):
    name = CharField(write_only=True, validators=[UniqueValidator(queryset=queryset)])
    surname = CharField(write_only=True, required=False)
    identification = CharField(
        write_only=True, required=False, validators=[UniqueValidator(queryset=queryset)]
    )
    address = CharField(write_only=True, required=False)
    nationality = CharField(write_only=True, required=False)
    date_of_birth = DateField(write_only=True, required=False)
    phone = CharField(write_only=True, required=False)


class UsuariosExcelSerializersView(Serializer):
    name = CharField()
    nationality = CharField()
    municipio = CharField()
    departamento = CharField()
    address = CharField()
    condicion_vulnerable = CharField()
    estado_civil = CharField()
    phone = CharField()
    phone2 = CharField()
    email = CharField()
    email2 = CharField()
    programa = CharField()
    sede = CharField()
    modalidad_grado = CharField()
    proyecto_grado = CharField()
    periodo_grado = CharField()
    numero_acta = CharField()
    numero_folio = CharField()
    saber_pro = CharField()
    direccion_intitucional = CharField()
    identification = CharField()
    document_type = CharField()
    genero = CharField()
  
class PersonCreatedSerializer(Serializer):
    fullname = CharField()
    
class PersonPonentesSerializers(Serializer):
    fullname = CharField(read_only=True)
    document = DocumentSerializersView(read_only=True)
    email = EmailField(read_only=True)
    phone = CharField(read_only=True)
    
class PersonAsistenciaSerializers(Serializer):
    id = IntegerField(read_only=True)
    fullname = CharField(read_only=True)
    email = EmailField(read_only=True)
    graduado = BooleanField(read_only=True)
    funcionario = BooleanField(read_only=True)


