"""
ASGI config for DjangoUI project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os
from Helpers.environment_decision_helper import EnvironmentDecisionHelper

from django.core.asgi import get_asgi_application

EnvironmentDecisionHelper.set_environment_django_settings()

application = get_asgi_application()
