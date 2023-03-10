# Generated by Django 4.0.5 on 2022-10-13 10:28

from datetime import datetime

import pytz
from django.db import migrations
from django.utils import timezone


def backfill_datetime(apps, schema_editor):
    Task = apps.get_model("soteria_atms.Task")
    tasks = Task.objects.all()
    for task in tasks:
        task.start_at_tem = timezone.make_aware(
            datetime.combine(task.date, task.start_at),
            timezone=pytz.timezone("Asia/Kolkata"),
        )
        task.end_at_tem = timezone.make_aware(
            datetime.combine(task.date, task.end_at),
            timezone=pytz.timezone("Asia/Kolkata"),
        )
        task.save(update_fields=["start_at_tem", "end_at_tem"])


class Migration(migrations.Migration):

    dependencies = [
        ("soteria_atms", "0015_task_end_at_tem_task_start_at_tem"),
    ]

    operations = [
        migrations.RunPython(backfill_datetime, reverse_code=migrations.RunPython.noop),
    ]
