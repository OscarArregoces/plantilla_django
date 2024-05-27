from django.urls import path

from django.urls import path


from src.application.auth_module.api.view.roles.views import RolesView

urlpatterns = [
    path("", RolesView.as_view()),
    path("<int:rol_id>/", RolesView.as_view()),
]
