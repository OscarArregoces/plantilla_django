from django.urls import path, re_path
from .users import  UserChangePasswordView
from django.conf.urls import include


from src.application.auth_module.api.view.users.route import Router
from src.application.auth_module.api.view.users.users import UserViewSet

router = Router()
router.register("", viewset=UserViewSet, basename="users")
urlpatterns = [
    path("", include(router.urls)),
    path("change/password/", UserChangePasswordView.as_view()),
]
