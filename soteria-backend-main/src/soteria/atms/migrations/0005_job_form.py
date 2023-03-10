# Generated by Django 4.0.5 on 2022-08-29 10:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("soteria_atms", "0004_remove_task_assign_to_remove_task_form_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="job",
            name="form",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="soteria_atms.form",
                verbose_name="form",
            ),
        ),
    ]