# Generated by Django 4.0.5 on 2022-11-18 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("soteria_atms", "0018_rename_end_at_tem_task_end_at_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="task",
            name="is_late_submission",
            field=models.BooleanField(blank=True, null=True, verbose_name="is late submission "),
        ),
    ]
