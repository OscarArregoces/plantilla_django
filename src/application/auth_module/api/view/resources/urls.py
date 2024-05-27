from src.application.auth_module.api.view.resources.views import ResourcesView
from ..modules import path

from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path("",  ResourcesView.as_view()),
    path("<int:recurso_id>/",  ResourcesView.as_view()),
]
