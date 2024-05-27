from rest_framework.routers import Route, SimpleRouter
from src.factory.auth_interactor import AuthViewSetFactory
from src.interfaces.routes.auth_module.user_route import router
from src.application.auth_module.models import User


class Router(SimpleRouter):
    router_base = router
    name_base = "user"
    model = User

    routes = [
        Route(
            url=router_base.get_url(f"{name_base}_get"),
            mapping=router_base.map(f"{name_base}_get"),
            initkwargs={
                "viewset_factory": AuthViewSetFactory,
                "http_method_names": ["get"],
                "model": model,
            },
            name="{basename}-list",
            detail=True,
        ),
        Route(
            url=router_base.get_url(f"{name_base}_post"),
            mapping=router_base.map(f"{name_base}_post"),
            initkwargs={
                "viewset_factory": AuthViewSetFactory,
                "http_method_names": ["post"],
                "model": model,
            },
            name="{basename}-create",
            detail=True,
        ),
        Route(
            url=router_base.get_url(f"{name_base}_put"),
            mapping=router_base.map(f"{name_base}_put"),
            initkwargs={
                "viewset_factory": AuthViewSetFactory,
                "http_method_names": ["put"],
                "model": model,
            },
            name="{basename}-update",
            detail=True,
        ),
        Route(
            url=router_base.get_url(f"{name_base}_all"),
            mapping=router_base.map(f"{name_base}_all"),
            initkwargs={
                "viewset_factory": AuthViewSetFactory,
                "http_method_names": ["get"],
                "model": model,
            },
            name="{basename}-all",
            detail=True,
        ),
    ]
