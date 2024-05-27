from ..modules import path


from django.conf.urls import include
from django.urls import path


from src.application.auth_module.api.view.genders.routers import GenderRouter
from src.application.auth_module.api.view.genders.views import GenderViewSet

router = GenderRouter()
router.register("", viewset=GenderViewSet, basename="gender")
urlpatterns = [path("", include(router.urls))]
