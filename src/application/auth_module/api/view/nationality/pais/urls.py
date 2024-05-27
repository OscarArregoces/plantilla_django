from django.urls import path

from src.application.auth_module.api.view.nationality.pais.view import PaisesView
urlpatterns = [
    path("pais/", PaisesView.as_view()),
]
