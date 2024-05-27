from django.urls import path
from src.application.auth_module.api.view.nationality.departamento.view import DepartamentosByPaisView, DepartamentosView

urlpatterns = [
    path("departamento/", DepartamentosView.as_view()),
    path("departamento/byPais/<int:pais_id>/", DepartamentosByPaisView.as_view()),
]
