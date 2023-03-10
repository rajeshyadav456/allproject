#!/usr/bin/env python
import os
import sys

# Add source directory to system path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soteria.conf.settings")
    os.environ.setdefault("DJANGO_CONFIGURATION", "Development")
    try:
        # from django.core.management import execute_from_command_line
        from configurations.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
