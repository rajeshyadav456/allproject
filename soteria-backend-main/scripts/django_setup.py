# -*- coding: utf-8 -*-
import os
import sys
from configurations import importer

# if django configuration is not setup/installed then do it
if not importer.installed:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soteria.conf.settings")
    os.environ.setdefault("DJANGO_CONFIGURATION", "Development")
    import configurations

    configurations.setup()
