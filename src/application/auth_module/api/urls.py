from django.urls import path, include
from src.application.constants import PATH_APP

app_name = "auth"


urlpatterns = [
    path("auth/", include(f"{PATH_APP}.auth_module.api.view.auth.urls")),
    path("users/", include(f"{PATH_APP}.auth_module.api.view.users.urls")),
    path("roles/", include(f"{PATH_APP}.auth_module.api.view.roles.urls")),
    path("resources/", include(f"{PATH_APP}.auth_module.api.view.resources.urls")),
    path("persons/", include(f"{PATH_APP}.auth_module.api.view.persons.urls")),
    path("genders/", include(f"{PATH_APP}.auth_module.api.view.genders.urls")),
    path("documents/", include(f"{PATH_APP}.auth_module.api.view.documents.urls")),
    path("security/", include(f"{PATH_APP}.auth_module.api.view.security.urls")),
    path("nationality/", include(f"{PATH_APP}.auth_module.api.view.nationality.urls")),
]
