from django.conf import settings
from django.template.context import RequestContext
import environ

# def customContextProcessor(request):
#     env = environ.Env()
#     URL_MEDIA = env("URL_MEDIA")
#     context = RequestContext(request)
#     context['url_media'] = URL_MEDIA
#     # context['url_media'] = settings.URL_MEDIA
#     return context