"""
WSGI config for dtf_bot project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dtf_bot.settings")

application = get_wsgi_application()
