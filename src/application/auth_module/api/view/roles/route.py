from rest_framework.routers import Route, SimpleRouter
from src.factory.auth_interactor import AuthViewSetFactory
from src.interfaces.routes.auth_module.role_route import router
from django.contrib.auth.models import Group


class Router(SimpleRouter):
    router_base = router
    name_base = "roles"
    model = Group

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
            url=router_base.get_url(f"{name_base}_related"),
            mapping=router_base.map(f"{name_base}_related"),
            initkwargs={
                "viewset_factory": AuthViewSetFactory,
                "http_method_names": ["get"],
                "model": model,
            },
            name="{basename}-related",
            detail=True,
        ),
        Route(
            url=router_base.get_url(f"{name_base}_delete"),
            mapping=router_base.map(f"{name_base}_delete"),
            initkwargs={
                "viewset_factory": AuthViewSetFactory,
                "http_method_names": ["delete"],
                "model": model,
            },
            name="{basename}-delete",
            detail=True,
        )
    ]
