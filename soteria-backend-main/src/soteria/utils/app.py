import os

from configurations import importer


def setup_app_config():
    # if django configuration is not setup/installed then do it
    if not importer.installed:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soteria.conf.settings")
        os.environ.setdefault("DJANGO_CONFIGURATION", "Development")
        import configurations

        configurations.setup()
