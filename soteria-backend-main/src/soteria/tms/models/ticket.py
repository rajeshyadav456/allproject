from django.db import models
from django.utils.translation import gettext_lazy as _

from soteria.db.models.base import DefaultFieldsModel, UUIDModel
from soteria.db.models.utils import sane_repr, sane_str


class TicketType(UUIDModel, DefaultFieldsModel):
    name = models.CharField(max_length=100, verbose_name=_("name"))
    description = models.CharField(max_length=100, verbose_name=_("description"))

    class Meta:
        app_label = "soteria_tms"
        db_table = "soteria_tms_ticket_type"
        verbose_name = _("ticket type")
        verbose_name_plural = _("ticket types")

    __repr__ = sane_repr("id", "name")
    __str__ = sane_str("id", "name")


class TicketLabel(UUIDModel, DefaultFieldsModel):
    name = models.CharField(max_length=100, verbose_name=_("name"))
    description = models.CharField(max_length=100, verbose_name=_("description"))

    class Meta:
        app_label = "soteria_tms"
        db_table = "soteria_tms_ticket_label"
        verbose_name = _("ticket label")
        verbose_name_plural = _("ticket labels")

    __repr__ = sane_repr("id", "name")
    __str__ = sane_str("id", "name")


class Priority(UUIDModel, DefaultFieldsModel):
    name = models.CharField(max_length=100, verbose_name=_("name"))
    description = models.CharField(max_length=100, verbose_name=_("description"))

    class Meta:
        app_label = "soteria_tms"
        db_table = "soteria_tms_priority"
        verbose_name = _("priority")
        verbose_name_plural = _("priorities")

    __repr__ = sane_repr("id", "name", "description")
    __str__ = sane_str("id", "name", "description")


class TicketActivity(UUIDModel, DefaultFieldsModel):
    class ActivityChoice(models.TextChoices):
        COMMENT = "comment", _("Comment")
        STATECHANGE = "statechange", _("Statechange")
        ASSIGNMENT = "assignment", _("Assignment")

    activity = models.CharField(
        max_length=100, choices=ActivityChoice.choices, verbose_name=_("activity")
    )
    ticket = models.ForeignKey(
        "soteria_tms.Ticket",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("ticket"),
    )

    class Meta:
        app_label = "soteria_tms"
        db_table = "soteria_tms_ticket_activity"
        verbose_name = _("ticket activity")
        verbose_name_plural = _("ticket activities")

    __repr__ = sane_repr("id", "name")
    __str__ = sane_str("id", "name")


class Ticket(UUIDModel, DefaultFieldsModel):
    class StatusChoice(models.TextChoices):
        OPEN = "open", _("Open")
        HOLD = "hold", _("Hold")
        RESOLVED = "resolved", _("Resolved")

    name = models.CharField(max_length=100, verbose_name=_("name"))
    status = models.CharField(
        max_length=100,
        choices=StatusChoice.choices,
        default=StatusChoice.OPEN,
        verbose_name=_("status"),
    )
    assign_to = models.ForeignKey(
        "soteria.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="assign_to"
    )
    assign_by = models.ForeignKey(
        "soteria.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="assign_by"
    )
    description = models.CharField(max_length=200, verbose_name=_("descripiton"))
    loction = models.ForeignKey(
        "soteria_orgs.Location",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("location"),
    )
    ticket_type = models.ForeignKey(
        "soteria_tms.TicketType",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("ticket type"),
    )
    ticket_label = models.ForeignKey(
        "soteria_tms.TicketLabel",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("ticket label"),
    )
    priority = models.ForeignKey(
        "soteria_tms.Priority",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("priority"),
    )

    class Meta:
        app_label = "soteria_tms"
        db_table = "soteria_tms_ticket"
        verbose_name = _("ticket")
        verbose_name_plural = _("tickets")

    __repr__ = sane_repr("id", "name")
    __str__ = sane_str("id", "name")
