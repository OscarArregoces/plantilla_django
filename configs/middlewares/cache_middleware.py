from django.middleware.cache import CacheMiddleware
from django.http import HttpRequest
from django.core.cache import cache


class MyCacheMiddleware(CacheMiddleware):
    def process_request(self, request: HttpRequest):
        cache_key = f"{request.user}-{request.session.session_key}"
        self.key_prefix = cache_key

        if self.should_cache_request(request):
            # return super().process_request(request)
            cache.set(cache_key,request)
        elif request.method in ["PUT", "DELETE", "POST"]:
            cache.delete(cache_key)
        return None

    def should_cache_request(self, request: HttpRequest):
        return request.method == "GET" and request.user.is_authenticated

    def process_response(self, request, response):
        response = super().process_response(request, response)
        return response
