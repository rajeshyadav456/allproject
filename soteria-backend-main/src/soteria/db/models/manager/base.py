from typing import Generic

from django.db import models

from soteria.db.models.manager import M
from soteria.db.models.manager.base_query_set import BaseQuerySet


class BaseManager(models.Manager.from_queryset(BaseQuerySet), Generic[M]):
    _queryset_class = BaseQuerySet
