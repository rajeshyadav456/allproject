# Generated by Django 4.0.5 on 2022-10-12 06:32

from django.db import migrations


def map_task_date(apps, schema_editor):
    Task = apps.get_model("soteria_atms", "Task")
    tasks = Task.objects.all()
    for task in tasks:
        task.date = task.created_at.date()
        task.save(update_fields=["date"])


class Migration(migrations.Migration):

    dependencies = [
        ("soteria_atms", "0011_task_date"),
    ]

    operations = [
        migrations.RunPython(map_task_date, reverse_code=migrations.RunPython.noop),
    ]
