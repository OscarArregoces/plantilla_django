from src.domain.routing import Route, Router
from src.domain.constants import (
    HTTP_VERB_GET,
    HTTP_VERB_POST,
    HTTP_VERB_DELETE,
    HTTP_VERB_PUT,
)
from src.interfaces.controllers.base_controller import BaseController

gender_router = Router()

gender_router.register(
    [
        Route(
            http_verb=HTTP_VERB_GET,
            path=r"$",
            controller=BaseController,
            method="get",
            name="genders_get",
        ),
        Route(
            http_verb=HTTP_VERB_POST,
            path=r"create/$",
            controller=BaseController,
            method="post",
            name="genders_post",
        ),
        Route(
            http_verb=HTTP_VERB_PUT,
            path="update/(?P<id>[0-9]+)/$",
            controller=BaseController,
            method="put",
            name="genders_put",
        ),
        Route(
            http_verb=HTTP_VERB_DELETE,
            path=r"delete/?(?P<id>[0-9]+)?/$",
            controller=BaseController,
            method="delete",
            name="genders_delete",
        ),
    ]
)
