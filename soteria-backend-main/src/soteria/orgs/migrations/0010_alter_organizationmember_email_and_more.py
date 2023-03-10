# Generated by Django 4.0.5 on 2022-12-22 11:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("soteria_orgs", "0009_alter_organizationmember_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organizationmember",
            name="email",
            field=models.EmailField(
                blank=True,
                max_length=254,
                validators=[django.core.validators.EmailValidator()],
                verbose_name="email address",
            ),
        ),
        migrations.AlterField(
            model_name="organizationmember",
            name="role",
            field=models.CharField(
                choices=[
                    ("client", "Client"),
                    ("executive", "Executive"),
                    ("supervisor", "Supervisor"),
                    ("staff", "Staff"),
                    ("leader", "Leader"),
                ],
                default="client",
                max_length=30,
                verbose_name="role",
            ),
        ),
        migrations.AlterField(
            model_name="organizationmember",
            name="token",
            field=models.CharField(
                blank=True, db_index=True, max_length=64, null=True, verbose_name="token"
            ),
        ),
        migrations.AlterField(
            model_name="organizationmember",
            name="token_expires_at",
            field=models.DateTimeField(
                blank=True, default=None, null=True, verbose_name="token expires at"
            ),
        ),
    ]
