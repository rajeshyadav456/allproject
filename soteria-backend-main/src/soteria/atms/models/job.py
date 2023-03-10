from django.contrib.postgres import fields as pg_fields
from django.db import models
from django.utils.translation import gettext_lazy as _
from timezone_field import TimeZoneField

from soteria.db.models.base import DefaultFieldsModel, UUIDModel
from soteria.db.models.utils import sane_repr, sane_str

WEEKDAYS_ABBR_MAPPING = {
    1: "Mon",
    2: "Tue",
    3: "Wed",
    4: "Thu",
    5: "Fri",
    6: "Sat",
    7: "Sun",
}


class JobType(UUIDModel, DefaultFieldsModel):
    name = models.CharField(max_length=100, blank=True, verbose_name=_("name"))
    description = models.CharField(max_length=200, blank=True, verbose_name=_("description"))
    is_active = models.BooleanField(default=True)

    class Meta:
        app_label = "soteria_atms"
        db_table = "soteria_atms_job_type"
        verbose_name = _("job type")
        verbose_name_plural = _("job types")

    __repr__ = sane_repr("id", "name")
    __str__ = sane_str("id", "name")


class Job(UUIDModel, DefaultFieldsModel):
    class TimeScale(models.TextChoices):
        DAILY = "daily", _("Daily")
        MONTHLY = "monthly", _("Monthly")
        QUARTERLY = "quarterly", _("Quarterly")

    name = models.CharField(max_length=200, blank=True, verbose_name=_("name"))
    description = models.CharField(max_length=300, blank=True, verbose_name=_("description"))
    asset = models.ForeignKey(
        "soteria_atms.Asset",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("asset"),
    )
    weekdays = pg_fields.ArrayField(
        models.PositiveSmallIntegerField(),
        size=7,
        null=True,
        blank=True,
        verbose_name=_("days"),
    )
    assign_to = models.ForeignKey(
        "soteria_orgs.OrganizationMember",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("assign to"),
    )
    location = models.ForeignKey(
        "soteria_orgs.Location",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("location"),
    )
    form = models.ForeignKey(
        "soteria_atms.Form",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("form"),
    )
    job_type = models.ForeignKey(
        "soteria_atms.JobType",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("job type"),
    )
    timezone = TimeZoneField(
        choices_display="WITH_GMT_OFFSET",
        verbose_name=_("timezone"),
    )
    time_ranges = pg_fields.ArrayField(
        models.TimeField(),
        null=True,
        blank=True,
        verbose_name=_("time ranges"),
    )
    duration = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name=_("duration"),
        help_text=_("Duration of one timeslot in minutes"),
    )
    time_scale = models.CharField(
        max_length=100,
        choices=TimeScale.choices,
        default=TimeScale.DAILY,
        verbose_name=_("time scale"),
    )
    start_at = models.DateTimeField(
        null=False, blank=False, db_index=True, verbose_name=_("start at")
    )
    end_at = models.DateTimeField(null=False, blank=False, db_index=True, verbose_name=_("end at"))

    class Meta:
        app_label = "soteria_atms"
        db_table = "soteria_atms_job"
        verbose_name = _("job")
        verbose_name_plural = _("jobs")

    __repr__ = sane_repr("id")
    __str__ = sane_str("id")

    @property
    def get_weekdays_abbr(self):
        return [WEEKDAYS_ABBR_MAPPING[d] for d in self.weekdays] if self.weekdays else ""

    @property
    def job_created_at(self):
        return str(self.created_at).split(" ")[0]
