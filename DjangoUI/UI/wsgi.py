"""
WSGI config for DjangoUI project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
from Helpers.environment_decision_helper import EnvironmentDecisionHelper

from django.core.wsgi import get_wsgi_application

EnvironmentDecisionHelper.set_environment_django_settings()

application = get_wsgi_application()
