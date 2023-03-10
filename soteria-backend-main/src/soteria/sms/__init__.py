from django.utils.connection import BaseConnectionHandler, ConnectionProxy
from django.utils.module_loading import import_string

from soteria.conf import settings
from soteria.sms.backends.base import BaseSMSBackend
from soteria.sms.exceptions import InvalidSMSBackendError

from .exceptions import *  # noqa


class SMSHandler(BaseConnectionHandler):
    settings_name = "SMS_CLIENTS"
    exception_class = InvalidSMSBackendError

    def create_connection(self, alias):
        params = self.settings[alias].copy()
        backend = params.pop("BACKEND")
        try:
            backend_cls = import_string(backend)
        except ImportError as e:
            raise InvalidSMSBackendError("Could not find backend '%s': %s" % (backend, e)) from e
        return backend_cls(params)

    def all(self, initialized_only=False):
        return [
            self[alias]
            for alias in self
            # If initialized_only is True, return only initialized caches.
            if not initialized_only or hasattr(self._connections, alias)
        ]


sms_backend_manager = SMSHandler()


default_sms_backend: BaseSMSBackend = ConnectionProxy(
    sms_backend_manager, settings.DEFAULT_SMS_CLIENT_ALIAS
)
