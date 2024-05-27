from rest_framework import status
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class BaseController:
    def __init__(self, repo, serializer) -> None:
        self.repo = repo
        self.serializer = serializer

    def get_filter_related(
        self, filter_param=None, related=None, prefetch=None, **kwargs
    ):
        resp = self.repo.get_filter_related(filter_param, related, prefetch, **kwargs)
        serializer = self.serializer(resp, many=True)
        return serializer.data, status.HTTP_200_OK

    def complex_filters(self, excludes: list = [], **kwargs):
        resp = self.repo.complex_filters(**kwargs)
        serializer = self.serializer(resp, many=True, excludes=excludes)
        return serializer.data, status.HTTP_200_OK

    def get_object(self, id, prefetch=None, related=None):
        resp = self.repo.get_instance(id, prefetch, related)
        serializer = self.serializer(resp)
        return serializer.data, status.HTTP_200_OK

    def get(self):
        resp = self.repo.get()
        serializer = self.serializer(resp, many=True)
        return serializer.data, status.HTTP_200_OK

    def get_all(self, related=None, prefetch=None):
        resp = self.repo.get_all(related, prefetch)
        serializer = self.serializer(resp, many=True)
        return serializer.data, status.HTTP_200_OK

    def post(self, data, extra={}):
        try:
            serializers = self.serializer(data=data)
            if serializers.is_valid():
                instance = serializers.save(**extra)
                return {
                    "message": "Success",
                    "id": instance.id,
                }, status.HTTP_201_CREATED
            return serializers.errors, status.HTTP_400_BAD_REQUEST
        except Exception as e:
            return e.args, status.HTTP_400_BAD_REQUEST

    def put(self, id: int, data):
        instance = self.repo.get_instance(id)

        if not instance:
            return "NOT FOUND", status.HTTP_400_BAD_REQUEST

        serializers = self.serializer(instance, data=data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return "Ok", status.HTTP_200_OK
        return serializers.errors, status.HTTP_400_BAD_REQUEST

    def filter_in(self, **kwargs):
        resp = self.repo.filter_in(**kwargs)
        serializer = self.serializer(resp, many=True)
        return serializer.data, status.HTTP_200_OK

    def delete(self, id, ids=None):
        if ids:
            err, valid = self.repo.bulk_delete(ids)

            if not valid:
                return err, status.HTTP_400_BAD_REQUEST

            return "Ok", status.HTTP_200_OK

        instance = self.repo.get_instance(id)

        if not instance:
            return "NOT FOUND", status.HTTP_400_BAD_REQUEST

        instance.visible = False
        instance.save()

        return "Ok", status.HTTP_200_OK
