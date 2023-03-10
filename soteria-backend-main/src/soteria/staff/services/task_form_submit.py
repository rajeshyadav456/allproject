from datetime import datetime, timedelta
from typing import Dict

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from soteria.atms.models import Task


def submit_task_form(task: Task, data: Dict) -> Task:
    """
    Submit form data
    : We assume that every submitted task has status of completed ,
    if task submit in given time range (Buffer of 15 mins) late_submit : False else True
    """
    now = datetime.now(timezone.utc)
    late_submit: bool = False
    if task.status == Task.Status.COMPLETED:
        raise serializers.ValidationError(_("Task already submitted."))

    if task.start_at.time() > now.time():
        raise serializers.ValidationError(_("You can not submit task now."))

    if (
        now.time()
        > (datetime.combine(task.end_at.date(), task.end_at.time()) + timedelta(minutes=15)).time()
    ):
        late_submit: bool = True

    task.status = Task.Status.COMPLETED
    task.is_late_submission = late_submit

    task.form_submission_data = data["schema"] or None
    task.completed_at = now

    task.save(
        update_fields=["form_submission_data", "status", "completed_at", "is_late_submission"]
    )

    return task
