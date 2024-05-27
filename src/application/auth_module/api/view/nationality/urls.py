from django.urls import path, include
from src.application.constants import PATH_APP

urlpatterns = [
     path("", include(f"{PATH_APP}.auth_module.api.view.nationality.ciudad.urls")),
     path("", include(f"{PATH_APP}.auth_module.api.view.nationality.departamento.urls")),
     path("", include(f"{PATH_APP}.auth_module.api.view.nationality.pais.urls")),
]
