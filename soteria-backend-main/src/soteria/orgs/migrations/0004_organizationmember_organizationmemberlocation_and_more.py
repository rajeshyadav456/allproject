# Generated by Django 4.0.5 on 2022-08-01 19:19

import uuid

import django.core.validators
import django.db.models.deletion
import model_utils.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("soteria", "0006_organization_alter_domain_tenant_delete_tenant"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("soteria_orgs", "0003_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrganizationMember",
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
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="created at"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, db_index=True, verbose_name="last updated at"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=254,
                        unique=True,
                        validators=[django.core.validators.EmailValidator()],
                        verbose_name="email address",
                    ),
                ),
                (
                    "mobile",
                    models.CharField(
                        blank=True,
                        max_length=18,
                        null=True,
                        unique=True,
                        verbose_name="mobile number",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="created by",
                    ),
                ),
            ],
            options={
                "verbose_name": "organization member",
                "verbose_name_plural": "organization members",
                "db_table": "soteria_org_member",
            },
        ),
        migrations.CreateModel(
            name="OrganizationMemberLocation",
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
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, db_index=True, verbose_name="created at"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True, db_index=True, verbose_name="last updated at"
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_created",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="created by",
                    ),
                ),
                (
                    "location",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="soteria_orgs.location"
                    ),
                ),
                (
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="soteria_orgs.organizationmember",
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="%(class)s_updated",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="last updated by",
                    ),
                ),
            ],
            options={
                "verbose_name": "organization member location",
                "verbose_name_plural": "organization member locations",
                "db_table": "soteria_org_member_location",
            },
        ),
        migrations.AddField(
            model_name="organizationmember",
            name="location",
            field=models.ManyToManyField(
                blank=True,
                through="soteria_orgs.OrganizationMemberLocation",
                to="soteria_orgs.location",
                verbose_name="location",
            ),
        ),
        migrations.AddField(
            model_name="organizationmember",
            name="organization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="soteria.organization",
                verbose_name="organization",
            ),
        ),
        migrations.AddField(
            model_name="organizationmember",
            name="updated_by",
            field=models.ForeignKey(
                blank=True,
                default=None,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="%(class)s_updated",
                to=settings.AUTH_USER_MODEL,
                verbose_name="last updated by",
            ),
        ),
        migrations.AddField(
            model_name="organizationmember",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="user",
            ),
        ),
    ]
