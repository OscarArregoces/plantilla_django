"""
File in which we have the middleware for Django for Authenticating API requests
"""
import json
import logging
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import HttpResponse
from configs.helpers.create_response import create_response
from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.exceptions import (
    InvalidToken,
    AuthenticationFailed,
    TokenBackendError,
    TokenError,
    exceptions,
)
from django.contrib.auth import get_user_model
import os
import re

User = get_user_model()

# Initialize logger
logger = logging.getLogger(__name__)
# Get JWT secret key

SECRET_KEY = os.environ.get("SECRET_OR_KEY")


class CustomMiddleware(MiddlewareMixin):

    """
    Custom Middleware Class to process a request before it reached the endpoint
    """

    def process_request(self, request):
        """
        Custom middleware handler to check authentication for a user with JWT authentication
        :param request: Request header containing authorization tokens
        :type request: Django Request Object
        :return: HTTP Response if authorization fails, else None
        """
        routes_free = [
            "/auth/login/",
            "/auth/register/",
            "/auth/refresh/",
            "/redoc/",
            "/admin/",
            "/__debug__/",
            "/media/",
            "/confirmar/asistencia/",
            ".*/generar/",
            ".*/grafica/",
            
            # ".*/test",
        ]

        match = re.search("|".join(routes_free), request.path)
        if match:
            return None

        jwt_token: str = request.headers.get("authorization", None)
        logger.info(f"request received for endpoint {str(request.path)}")

        # If token Exists
        if jwt_token:
            try:
                tokenUser, _ = JWTAuthentication.authenticate(
                    JWTAuthentication(), request
                )
                user = tokenUser

                if not tokenUser.is_authenticated:
                    response, code, _ = create_response(
                        401, "Unauthorized", {"message": "User not in session"}
                    )
                    return HttpResponse(
                        json.dumps(response),
                        content_type="application/json",
                        status=code,
                    )

                if not user:
                    response, code = create_response(
                        401, "Unauthorized", {"message": "User not found"}
                    )
                    return HttpResponse(json.dumps(response), status=code)

                request.user = tokenUser
                return None
            except (
                InvalidToken,
                AuthenticationFailed,
                TokenBackendError,
                TokenError,
                exceptions.ValidationError,
                exceptions.APIException,
                exceptions.PermissionDenied,
            ):
                response, code, _ = create_response(
                    401,
                    "Unauthorized",
                    "Authorization has failed, Please send valid token",
                )
                logger.info(f"Response {response}")

                return HttpResponse(
                    json.dumps(response), content_type="application/json", status=code
                )
            except Exception as e:
                return HttpResponse(e.args, status=400)
        else:
            response, code, _ = create_response(
                401, "Unauthorized", "Authorization not found, Please send valid token"
            )
            logger.info(f"Response {response}")
            return HttpResponse(
                json.dumps(response), content_type="application/json", status=code
            )

    def process_response(self, request, response):
        return response
