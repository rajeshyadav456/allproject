# Generated by Django 4.0.5 on 2022-12-15 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("soteria_atms", "0024_remove_job_start_from_job_end_at_job_start_at_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="job",
            name="end_at",
            field=models.DateTimeField(db_index=True, verbose_name="end at"),
        ),
        migrations.AlterField(
            model_name="job",
            name="start_at",
            field=models.DateTimeField(db_index=True, verbose_name="start at"),
        ),
        migrations.AlterField(
            model_name="job",
            name="time_scale",
            field=models.CharField(
                choices=[("daily", "Daily"), ("monthly", "Monthly"), ("quaterly", "Quaterly")],
                default="daily",
                max_length=100,
                verbose_name="time scale",
            ),
        ),
    ]
