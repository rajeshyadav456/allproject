# Generated by Django 3.2.4 on 2021-07-22 12:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_usernotifications_dateadded'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usernotifications',
            name='DateAdded',
            field=models.DateTimeField(default=datetime.datetime(2021, 7, 22, 12, 27, 23, 887678)),
        ),
    ]