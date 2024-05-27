from django.apps import AppConfig

AUTO_FIELD = "django.db.models.BigAutoField"


PATH_APP = "src.application"


class DefaultConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = f"{PATH_APP}.default"
    label = "default"
    verbose_name = "Default"


class AuthConfig(AppConfig):
    default_auto_field = AUTO_FIELD
    name = f"{PATH_APP}.auth_module"
    label = "auth"
    verbose_name = "Auth"


class EncuestasConfig(AppConfig):
    default_auto_field = AUTO_FIELD
    name = f"{PATH_APP}.encuestas"
    label = "encuestas"
    verbose_name = "Encuestas"


class EventosConfig(AppConfig):
    default_auto_field = AUTO_FIELD
    name = f"{PATH_APP}.eventos"
    label = "eventos"
    verbose_name = "Eventos"

class ReportesConfig(AppConfig):
    default_auto_field = AUTO_FIELD
    name = f"{PATH_APP}.reportes"
    label = "reportes"
    verbose_name = "Reportes"
