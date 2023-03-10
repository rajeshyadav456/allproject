# Generated by Django 4.0.5 on 2022-12-15 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("soteria_orgs", "0008_organizationmember"),
    ]

    operations = [
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
            ),
        ),
    ]
