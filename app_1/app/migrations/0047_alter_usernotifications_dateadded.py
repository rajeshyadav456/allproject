# Generated by Django 3.2.7 on 2021-09-27 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0046_auto_20210909_0745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usernotifications',
            name='DateAdded',
            field=models.DateTimeField(default='2021 14 09/27/21 - 07:14:39'),
        ),
    ]
