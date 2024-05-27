from src.domain.routing import Route, Router
from src.domain.constants import (
    HTTP_VERB_GET,
    HTTP_VERB_POST,
    HTTP_VERB_PUT,
)
from src.interfaces.controllers.auth_module.auth_controller import AuthModuleController

router = Router()

name_base = "user"

router.register(
    [
        Route(
            http_verb=HTTP_VERB_GET,
            path=r"$",
            controller=AuthModuleController,
            method="get",
            name=f"{name_base}_get",
        ),
        Route(
            http_verb=HTTP_VERB_POST,
            path=r"create/$",
            controller=AuthModuleController,
            method="post",
            name=f"{name_base}_post",
        ),
        Route(
            http_verb=HTTP_VERB_PUT,
            path="update/(?P<id>[0-9]+)/$",
            controller=AuthModuleController,
            method="put",
            name=f"{name_base}_put",
        ),
        Route(
            http_verb=HTTP_VERB_GET,
            path="internal/$",
            controller=AuthModuleController,
            method="get_users",
            name=f"{name_base}_all",
        ),
    ]
)
