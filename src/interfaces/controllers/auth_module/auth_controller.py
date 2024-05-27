from unittest import result
from src.interfaces.controllers.base_controller import BaseController
from django.contrib.auth.models import Group, Permission
from django.db.models import Prefetch
from src.application.auth_module.models import Persons, Resources, Resources_roles
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from configs.helpers.menu_resources import menuResources


class AuthModuleController(BaseController):
    def __init__(self, repo, serializer) -> None:
        super().__init__(repo, serializer)

    def get_roles(self, group):
        excluded_apps = {
            "admin",
            "auth",
            "contenttypes",
            "sessions",
            "authtoken",
            "token_blacklist",
            "resources_roles",
            "persons",
            "resources",
            "respuesta",
            "redessociales",
            "votoanuncio",
            "mensajes",
            "answeruser",
            "inscripcion",
        }

        content_types = ContentType.objects.exclude(
            Q(model__in=excluded_apps) | Q(app_label__in=excluded_apps)
        ).values("app_label", "model")
        permissions_data = {}

        model_gestionar = [
            "eventosarea",
            "subareaeventos",
            "tipoevento",
            "asistencia",
            "tipomomento",
            "tipopqrs",
            "tipopqrs",
            "asignacion",
            "votoanuncio",
            "tiposcapacitaciones",
            "subcategoria",
            "redessociales",
            "genders",
            "faculties",
            "document_types",
            "programs",
            "headquarters",
            "user",
            "categoria",
            "question",
            "answer",
        ]
        group = Group.objects.prefetch_related(
            Prefetch(
                "permissions",
                Permission.objects.all().select_related("content_type"),
            ),
        ).get(pk=group)

        group_permissions_query = group.permissions.all()
        group_permissions_model = set(
            [x.content_type.model for x in group_permissions_query]
        )
        group_permissions_label = [
            x.content_type.app_label for x in group_permissions_query
        ]

        for content_type in content_types:
            app_label = content_type["app_label"]
            model = content_type["model"]

            if app_label not in permissions_data:
                permissions_data[app_label] = {}

            permissions_data[app_label][model] = []
            if (
                model in permissions_data[app_label]
                and model in group_permissions_model
            ):
                if model in model_gestionar:
                    permissions_data[app_label][model] = ["gestionar"]
                else:
                    permissions_data[app_label][model] = [
                        permission.name
                        for permission in group_permissions_query.filter(
                            content_type__model=model
                        )
                    ]

        permissions_data.setdefault("admin", {})["roles"] = []
        permissions_data.setdefault("classified_advertisements", {})["detalles"] = []

        if "mensajes" in group_permissions_model:
            permissions_data["classified_advertisements"]["detalles"] = ["gestionar"]

        if "auth" in group_permissions_label:
            permissions_data["admin"]["roles"] = ["gestionar"]

        return permissions_data, 200

    def get_users(self, internal=True):
        queryset = (
            Persons.objects.select_related("user", "document_type", "gender_type")
            .prefetch_related(Prefetch("user__groups", Group.objects.all()))
            .filter(user__is_staff=internal)
            .order_by("user__id")
        )

        list_user = []

        for i in queryset:
            user_groups = i.user.groups.values("name", "id") if i.user else []
            list_user.append(
                {
                    "id": i.user.pk,
                    # "email": i.user.email if i.user else None,
                    "persona": {
                        "name": i.name,
                        "surname": i.surname,
                        "identification": i.identification,
                        "address": i.address,
                        "nationality": i.nationality,
                        "phone": i.phone,
                        "gender": (
                            {"name": i.gender_type.name, "id": i.gender_type.pk}
                            if i.gender_type
                            else None
                        ),
                        "document": (
                            {
                                "id": i.document_type.pk,
                                "name": i.document_type.name,
                            }
                            if i.document_type
                            else None
                        ),
                        "date_of_birth": i.date_of_birth if i.date_of_birth else "",
                    },
                    "groups": list(user_groups),
                }
            )

        return list_user, 200

    def delete_roles(self, id, ids=None):
        try:
            if ids:
                Group.objects.filter(pk__in=ids).delete()
                return "Ok", 200

            group = self.repo.get_instance(id)
            group.delete()

            return "Ok", 200

        except Exception as e:
            return e.args, 400

    def create_many(self, resources):
        try:

            resources_new = []

            id_last_resources = 0
            last = Resources.objects.last()

            if last:
                id_last_resources = last.pk + 1

            menuResources(
                resources,
                resources_new,
                Resources,
                id_last_resources,
            )

            resources_new = Resources.objects.bulk_create(resources_new)
            return "Ok", 200
        except Exception as e:
            return e.args, 404

    def resources_role(self, rol):
        resources = Resources.objects.filter(roles=rol)
        serializer = self.serializer(resources, many=True)
        return serializer.data, 200
