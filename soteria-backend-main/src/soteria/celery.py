from celery import Celery, Task
from django.conf import settings

from soteria.apps import setup_app_config
from soteria.utils.celery import TransactionAwareTaskMixin

setup_app_config()


class BaseTask(TransactionAwareTaskMixin, Task):
    pass


app = Celery("soteria", task_cls="soteria.celery:BaseTask")

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
