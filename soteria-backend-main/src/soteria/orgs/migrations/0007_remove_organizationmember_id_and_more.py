# Generated by Django 4.0.5 on 2022-08-18 10:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("soteria", "0008_userorganization"),
        ("soteria_orgs", "0006_organizationmember_token_and_more"),
    ]

    operations = [migrations.DeleteModel(name="OrganizationMember")]
