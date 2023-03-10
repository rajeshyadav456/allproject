# Generated by Django 4.0.5 on 2022-08-18 09:01

import uuid

import django.db.models.deletion
import model_utils.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("soteria", "0007_alter_resetpasswordticket_client_ua_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserOrganization",
            fields=[
                (
                    "id",
                    model_utils.fields.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="id",
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="soteria.organization",
                        verbose_name="organization",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
            options={
                "verbose_name": "user organization",
                "verbose_name_plural": "user organizations",
                "db_table": "soteria_user_organization",
            },
        ),
    ]