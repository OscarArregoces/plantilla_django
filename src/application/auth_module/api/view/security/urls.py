from django.urls import path

from .security import (
    SecurityRolesPerson,
    SecurityRolesResource,
)

urlpatterns = [
    path("addRoleByPerson/", SecurityRolesPerson.as_view()),
    path("addResourcesByRol/", SecurityRolesResource.as_view()),
    path("getResourcesByRol/<int:rol_id>/", SecurityRolesResource.as_view()),
]
