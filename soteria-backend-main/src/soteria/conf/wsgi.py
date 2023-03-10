"""
WSGI config for soteria project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soteria.conf.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Development")

from configurations.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()
