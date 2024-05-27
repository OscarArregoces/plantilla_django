from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework.generics import UpdateAPIView
from rest_framework import status
from configs.helpers.PaginationView import DecoratorPaginateView

from ...serializers.user.users_serializers import (
    UserSerializers,
    CreateUserSerializers,
    UserChangePassword,
)
from ....models import Persons, User
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from typing import Optional
from src.factory.auth_interactor import AuthViewSetFactory
import pandas as pd

from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.db import transaction
from datetime import datetime
import json
import os
from django.db.models import Prefetch

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


# @method_decorator(cache_page(CACHE_TTL), name="dispatch")
class UserViewSet(ViewSet):
    viewset_factory: AuthViewSetFactory = None
    http_method_names: Optional[list[str]] = []
    model = None

    def get_serializer_class(self):
        if self.action in ["get", "get_all"]:
            return UserSerializers
        return CreateUserSerializers

    @property
    def controller(self):
        return self.viewset_factory.create(self.model, self.get_serializer_class())

    def get(self, request, *args, **kwargs):
        payload, status = self.controller.get_users(False)
        return Response(data=payload, status=status)

    def post(self, request, *args, **kwargs):
        payload, status = self.controller.post(request.data)
        return Response(data=payload, status=status)

    def put(self, request, *args, **kwargs):
        instance_id = kwargs.get("id", "")
        payload, status = self.controller.put(int(instance_id), request.data)
        return Response(data=payload, status=status)

    def delete(self, request, *args, **kwargs):
        instance_id = kwargs.get("id", "")

        if "ids" in request.data:
            payload, status = self.controller.delete(
                None, request.data.get("ids", None)
            )
            return Response(data=payload, status=status)

        payload, status = self.controller.delete(int(instance_id), request.data)
        return Response(data=payload, status=status)

    def get_users(self, request, *args, **kwargs):
        payload, status = self.controller.get_users()
        return Response(data=payload, status=status)


class UserChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def get_object(self):
        try:
            request_user = self.kwargs["pk"]
            user = User.objects.get(pk=request_user)
            return user
        except (User.DoesNotExist, TypeError):
            return None
        except (BaseException, TypeError) as e:
            return None

    def perform_update(self, serializer):
        if "original_password" in self.request.data:  # type: ignore
            password = make_password(self.request.data["password"])  # type: ignore
            serializer.save(password=password)
        else:
            serializer.save()

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        user = request.user

        if user is None:
            return Response("User don't exist", status.HTTP_400_BAD_REQUEST)  # type: ignore

        if "original_password" not in self.request.data:  # type: ignore
            return Response("Password Error", status.HTTP_400_BAD_REQUEST)

        if not user.check_password(request.data["original_password"]):
            return Response("Password is not correct.", status.HTTP_400_BAD_REQUEST)

        user_serializers = UserChangePassword(user, data=request.data, partial=partial)

        try:
            if user_serializers.is_valid():
                self.perform_update(user_serializers)
                return Response("Password Change", status.HTTP_200_OK)
            return Response(user_serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        except (AttributeError, Exception) as e:
            return Response(e.args, status.HTTP_400_BAD_REQUEST)
         