import pytest
import requests
from django.test.client import Client
from rest_framework_simplejwt.tokens import RefreshToken
from src.application.pqrs.models.models import Pqrs, TipoPqrs
from src.application.eventos.models.models import EventosArea
from django.urls import reverse
import environ
env = environ.Env()

username = "admin"
password = "12345678"


@pytest.fixture
def user_token(client, django_user_model):
    client.login(username=username, password=password)
    user = django_user_model.objects.get(username=username)
    refresh = RefreshToken.for_user(user=user)
    return str(refresh.access_token)


@pytest.fixture
def user_token_request(client, django_user_model):
    response = requests.post(
        "http://44.203.185.252/auth/login/",
        data={"username": username, "password": password},
    )

    response_content = response.json()
    token = response_content["data"]["token"]["access"]
    return token


@pytest.fixture
def create_tipo():
    return TipoPqrs.objects.create(tipo="Queja")


@pytest.fixture
def create_pqrs(create_tipo):
    return Pqrs.objects.create(
        tipopqrs_id=create_tipo.pk,
        persona_id=1,
        description="description",
        titulo="titulo",
        userCreate_id=1,
    )


@pytest.fixture
def PQRS_Creatre(**kwargs):
    def _factory_create(**kwargs):
        persona_id = kwargs.pop("persona_id", 1)
        description = kwargs.pop("description", "description")
        titulo = kwargs.pop("titulo", "titulo")
        tipopqrs_id = kwargs.pop("tipopqrs_id", 1)

        return Pqrs.objects.create(
            persona_id=persona_id,
            description=description,
            titulo=titulo,
            tipopqrs_id=tipopqrs_id,
            userCreate_id=1,
        )

    return _factory_create


@pytest.fixture
def create_pqrs_list(request, PQRS_Creatre, create_tipo):
    PQRS_LIST = []

    pqrs = request.param
    for i in pqrs:
        PQRS_LIST.append(
            PQRS_Creatre(
                persona_id=i[1],
                description=i[0],
                titulo=[2],
                tipopqrs_id=create_tipo.pk,
                userCreate_id=1,
            )
        )
    return PQRS_LIST


@pytest.fixture
def create_areas_factory(**kwargs):
    def _create_factory(**kwargs):
        name = kwargs.get("name")
        return EventosArea.objects.create(name=name)

    return _create_factory


@pytest.fixture
def areas(request, create_areas_factory):
    areas = request.param
    list_areas = []
    for i in areas:
        list_areas.append(create_areas_factory(name=i))
    return list_areas


@pytest.fixture
def respuesta_create(client, create_pqrs, user_token):
    client.post(
        reverse("pqrs:respuesta:respuesta-create"),
        data={"pqrs": create_pqrs.pk, "descripcion": "descripcion"},
        HTTP_AUTHORIZATION=f"Bearer {user_token}",
    )

    return create_pqrs.titulo


@pytest.fixture
def clear_cache(client, user_token):
    client.get(
        reverse("clear-cache"),
        HTTP_AUTHORIZATION=f"Bearer {user_token}",
    )
