from datetime import datetime, timedelta
from typing import Dict, List

from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from soteria.atms.models import Asset, Form, Job, Task
from soteria.orgs.models import Location, OrganizationMember


def is_job_time_ranges_overlap(time_ranges: List, duration: str) -> bool:
    now = datetime.now()
    for time_range in time_ranges:
        end_at = datetime.combine(now.today(), time_range) + timedelta(minutes=int(duration))
        for _time_range in time_ranges:
            if time_range < _time_range < end_at.time():
                return False
    return True


def create_job(
    asset: Asset,
    assign_to: OrganizationMember,
    location: Location,
    form: Form,
    time_ranges: List[str],
    duration: str,
    weekdays: List[int] = None,
    job_type: str = None,
    name: str = None,
    description: str = None,
    timezone: str = None,
    start_at: str = None,
    end_at: str = None,
    time_scale: str = None,
):
    """
    Creating Job
    :We can create as many job related to a `asset`.
    """
    if not is_job_time_ranges_overlap(time_ranges, duration):
        raise serializers.ValidationError(_("Time ranges overlap."))

    if not timezone:
        timezone = settings.DEFAULT_JOB_TIMEZONE

    job = Job.objects.get_or_create(
        asset=asset,
        assign_to=assign_to,
        location=location,
        form=form,
        name=name,
        time_ranges=time_ranges,
        duration=duration,
        weekdays=weekdays,
        job_type=job_type,
        description=description,
        timezone=timezone,
        start_at=start_at,
        end_at=end_at,
        time_scale=time_scale,
    )[0]
    return job


def update_task_name_for_job(name: str, job: Job):
    tasks = Task.objects.filter(job=job).all()
    for task in tasks:
        task.name = name
        task.save(update_fields=["name"])
    return


def update_job_details(job: Job, data: Dict):
    """
    Update job details
    """
    time_ranges = data.get("time_ranges")
    duration = data.get("duration")
    name = data.get("name")
    if not duration:
        duration = job.duration

    if time_ranges:
        if not is_job_time_ranges_overlap(time_ranges, duration):
            raise serializers.ValidationError(_("Time ranges overlap."))

    if name:
        # updating all existing task name
        update_task_name_for_job(name, job)

    update_fields = []
    for field, value in data.items():
        setattr(job, field, value)
        update_fields.append(field)

    if update_fields:
        job.save(update_fields=update_fields)

    return job


def deactivate_job(job: Job):
    """
    Deleting job
    """
    Job.objects.filter(id=job.id).delete()
