from src.application.auth_module.api.serializers.person.persons_serializers import PersonAsistenciaSerializers, PersonCreatedSerializer, PersonPonentesSerializers, PersonsSimpleSerializersView
from ..roles.roles_serializers import GroupSerializer
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from ..customValidators.usersValidators import UserValidatorBefore
from src.application.auth_module.models import Persons, Document_types, Genders
from django.db.transaction import atomic, rollback

User = get_user_model()



class UserSerializersSimple(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    # email = serializers.EmailField(read_only=True)

    class Meta:
        # fields = ("username", "email")
        fields = ("username")

    def __init__(self, instance=None, data=..., **kwargs):
        expands = kwargs.pop("expands", True)
        meta = kwargs.pop("meta", False)
        super().__init__(instance, data, **kwargs)

        if not expands:
            self.fields.pop("username")


class UserSerializers(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    surname = serializers.CharField(read_only=True)
    # email = serializers.CharField(read_only=True)
    groups = GroupSerializer(read_only=True, many=True)

    class Meta:
        fields = "__all__"


class CreateUserSerializers(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    person_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        try:
            with atomic():
                
                instance.username = validated_data.get("username", instance.username)
                # instance.email = validated_data.get("email", instance.email)

                person = Persons.objects.get(user__id=instance.pk)
                persona = validated_data.get("persona", {})

                person.name = persona.get("name", person.name)
                person.surname = persona.get("surname", person.surname)
                person.identification = persona.get(
                    "identification", person.identification
                )
                person.address = persona.get("address", person.address)
                person.nationality = persona.get("nationality", person.nationality)
                person.date_of_birth = persona.get(
                    "date_of_birth", person.date_of_birth
                )
                person.phone = persona.get("phone", person.phone)

                new_document_type_id = persona.get("document_type")
                if new_document_type_id:
                    new_document_type = Document_types.objects.get(
                        pk=new_document_type_id
                    )
                    person.document_type = new_document_type

                gender_type = persona.get("gender_type")
                if gender_type:
                    new_document_type = Genders.objects.get(pk=gender_type)
                    person.gender_type = new_document_type

                print("PASO")

                person.save()
                instance.save()
                return instance
        except Exception as e:
            rollback()
            raise e


class UserSerializersSimpleRegister(serializers.ModelSerializer):
    username = serializers.SlugField(
        max_length=100, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ("username", "password", "email", "first_name", "last_name")
        validators = [UserValidatorBefore()]


class UserChangePassword(serializers.Serializer):
    password = serializers.CharField()
    original_password = serializers.CharField()

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.password = validated_data.get("password", instance.password)
        instance.save()
        return instance


class UserCreatedSerializer(serializers.Serializer):
    person = PersonCreatedSerializer(read_only=True)
    
class UserPonentesSerializer(serializers.Serializer):
    person = PersonPonentesSerializers(read_only=True)
    
class UserAsistenciaSerializer(serializers.Serializer):
    person = PersonAsistenciaSerializers(read_only=True)
    