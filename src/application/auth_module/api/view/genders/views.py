from ..modules import Response
from src.application.auth_module.api.serializers.gender.gender_Serializers import (
    GenderSerializers,
    GenderSerializersView,
)
from rest_framework.viewsets import ViewSet
from typing import Optional
from src.factory.base_interactor import BaseViewSetFactory
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


# @method_decorator(cache_page(CACHE_TTL), name='dispatch')
class GenderViewSet(ViewSet):
    viewset_factory: BaseViewSetFactory = None
    http_method_names: Optional[list[str]] = []
    model = None

    serializer_class = GenderSerializers

    def get_serializer_class(self):
        if self.action in ["get"]:
            return GenderSerializersView
        return GenderSerializers

    @property
    def controller(self):
        return self.viewset_factory.create(self.model, self.get_serializer_class())

    def get(self, request, *args, **kwargs):
        payload, status = self.controller.get()
        return Response(data=payload, status=status)

    def post(self, request, *args, **kwargs):
        payload, status = self.controller.post(request.data)
        return Response(data=payload, status=status)

    def put(self, request, *args, **kwargs):
        instance_id = kwargs.get("id", "")
        payload, status = self.controller.put(int(instance_id), request.data)
        return Response(data=payload, status=status)

    def delete(self, request, *args, **kwargs):
        document_id = kwargs.get("id", "")

        if "ids" in request.data:
            payload, status = self.controller.delete(
                None, request.data.get("ids", None)
            )
            return Response(data=payload, status=status)

        payload, status = self.controller.delete(int(document_id), request.data)
        return Response(data=payload, status=status)
