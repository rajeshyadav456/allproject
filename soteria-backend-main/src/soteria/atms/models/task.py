from django.db import models
from django.utils.translation import gettext_lazy as _

from soteria.db.models.base import DefaultFieldsModel, UUIDModel
from soteria.db.models.utils import sane_repr, sane_str


class Task(UUIDModel, DefaultFieldsModel):
    class Status(models.TextChoices):
        COMPLETED = "completed", _("Completed")
        PENDING = "pending", _("Pending")
        OVERDUE = "overdue", _("Overdue")

    name = models.CharField(max_length=200, blank=True, verbose_name=_("name"))
    job = models.ForeignKey("soteria_atms.Job", on_delete=models.CASCADE, verbose_name=_("job"))
    status = models.CharField(
        max_length=100, choices=Status.choices, default=Status.PENDING, verbose_name=_("status")
    )
    is_late_submission = models.BooleanField(
        blank=True, null=True, verbose_name=_("is late submission ")
    )
    completed_at = models.DateTimeField(blank=True, null=True, verbose_name=_("completed at"))
    form_submission_data = models.JSONField(
        null=True, blank=True, verbose_name=_("form submission data")
    )
    start_at = models.DateTimeField(null=True, blank=True, verbose_name=_("start at"))
    end_at = models.DateTimeField(null=True, blank=True, verbose_name=_("end at"))

    class Meta:
        app_label = "soteria_atms"
        db_table = "soteria_atms_task"
        verbose_name = _("task")
        verbose_name_plural = _("tasks")

    __repr__ = sane_repr("id", "job_id", "status")
    __str__ = sane_str("id", "job_id", "status")
