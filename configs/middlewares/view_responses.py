from django.http import HttpResponse, JsonResponse

from src.application.auth_module.models import User
from ..helpers.create_response import create_response
import json
from django.db.utils import IntegrityError
import re
from django.core.cache import cache
import logging
import time
from datetime import datetime

logging.basicConfig(
    filename="example.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(name)s:%(message)s",
)


class CustomResponseMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # match = re.search("|".join(routes_free), request.path)
        routes_media = ["/media/", ".*/generar/",".*/grafica/", ".*/generar-reporte", ".*/descargar"]

        if re.match("|".join(routes_media), request.path):
            return HttpResponse(
                response, content_type=response.headers["Content-type"], status=200
            )
        try:
            decode = response.getvalue().decode()

            match = re.search(r"^[\d+]\s(.+)", decode)
            if match or type(decode) is list and decode[0].isdigit():
                decode = ["".join(x) for x in decode]
                parseResponse, code, render = create_response(
                    response.status_code, "Ok", decode, request.path, request.method
                )
                return HttpResponse(
                    json.dumps(parseResponse),
                    content_type="application/json",
                    status=code,
                )
            # if request.method in ["POST", "PUT", "DELETE"]:
            #     cache.clear()
            parseResponse, code, render = create_response(
                response.status_code, "Ok", decode, request.path, request.method
            )
            if render:
                return HttpResponse(
                    parseResponse, content_type="text/html", status=code
                )

            return HttpResponse(
                json.dumps(parseResponse), content_type="application/json", status=code
            )
        except (Exception, IntegrityError) as e:
            return JsonResponse(
                {"Error": "Unexpected error", "info": e.args},
                safe=False,
                status=500,
            )

    def process_exception(self, request, exception):
        return HttpResponse(exception, status=500)