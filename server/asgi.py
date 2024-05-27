"""
ASGI config for centro project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
import environ

env = environ.Env()
ENV = env("ENV")

APPS = f"settings.{ENV}"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", APPS)

application = get_asgi_application()
