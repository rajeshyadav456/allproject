import logging
from datetime import datetime, timedelta

from django.conf import settings
from django.db import connection
from django.utils import timezone

from soteria.atms.models import Job, Task
from soteria.models import Organization
from soteria.tasks.base import instrumented_task

logger = logging.getLogger(__name__)


def set_current_tenant(org_id: str):
    """
    method to set current organization i,e tenant
    """
    organization = Organization.objects.get(id=org_id)
    connection.set_tenant(organization)
    return


def create_task(job: Job):
    now = datetime.now(timezone.utc)
    for job_time in job.time_ranges:
        start_at = timezone.make_aware(
            value=datetime.combine(now.date(), job_time), timezone=job.timezone
        )
        end_at = timezone.make_aware(
            value=datetime.combine(now.date(), job_time), timezone=job.timezone
        ) + timedelta(minutes=int(job.duration))
        Task.objects.create(
            name=job.name,
            job=job,
            start_at=start_at,
            end_at=end_at,
        )


@instrumented_task(name="soteria.atms.tasks.schedule_tasks_for_job")
def schedule_tasks_for_job(job_id: str, org_id: str):
    set_current_tenant(org_id)
    job = Job.objects.get(id=job_id)
    now = datetime.now(timezone.utc)
    if job.start_at <= now <= job.end_at:
        # current weekday addr i.e 'Mon', 'Tue'
        curr_abbr = now.strftime("%A")[:3]
        task_filters = {"job": job}
        cond = {
            "daily": {"created_at__date": now.date()}
            if curr_abbr in job.get_weekdays_abbr
            else None,
            "monthly": {"created_at__month": now.month},
            "quaterly": {"created_at__quarter": (now.month - 1) // 3 + 1},
        }
        filters = cond.get(job.time_scale)
        if filters is not None:
            task_filters.update(filters)
            if not Task.objects.filter(**task_filters).exists():
                create_task(job)


@instrumented_task(name="soteria.atms.tasks.scheduler_for_org_jobs")
def scheduler_for_org_jobs(org_id: str):
    """
    get all jobs for organization and set tasks to create `Task` from `Job`.
    """
    set_current_tenant(org_id)
    jobs = Job.objects.all()
    if not jobs:
        return
    # TODO: Add support for task start from

    for job in jobs:
        schedule_tasks_for_job.delay(job.id, org_id)


@instrumented_task(name="soteria.atms.tasks.create_job_tasks")
def create_job_tasks():
    """
    Scheduler for organization jobs.
    """
    # getting all organization excluding `public` schema.
    organizations = Organization.objects.filter(status=Organization.Status.ACTIVE.value).exclude(
        schema_name=settings.PUBLIC_SCHEMA_NAME
    )

    for organization in organizations:
        logger.info(f"Setting organization({organization}) for task schedule")
        scheduler_for_org_jobs.delay(organization.id)


@instrumented_task(name="soteria.atms.tasks.schedule_tasks_for_set_task_status_overdue")
def schedule_tasks_for_set_task_status_overdue(org_id: str):
    set_current_tenant(org_id)
    curr_date = datetime.now().date()

    tasks = Task.objects.filter(status=Task.Status.PENDING)
    for task in tasks:
        if task.created_at.date() < curr_date:
            logger.info(f"Update Task as overdue {task} ")
            task.status = Task.Status.OVERDUE
            task.save(update_fields=["status"])


@instrumented_task(name="soteria.atms.tasks.set_daily_task_as_overdue")
def set_daily_task_as_overdue():
    """
    Schedular To set task status as overdue if not submitted on created date.
    """
    # getting all organization excluding `public` schema.
    organizations = Organization.objects.filter(status=Organization.Status.ACTIVE.value).exclude(
        schema_name=settings.PUBLIC_SCHEMA_NAME
    )
    for organization in organizations:
        logger.info(f"Setting organization({organization}) for task schedule")
        schedule_tasks_for_set_task_status_overdue.delay(organization.id)
