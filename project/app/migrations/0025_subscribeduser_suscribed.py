# Generated by Django 3.2.7 on 2021-12-13 04:34

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_rename_subscribeddate_subscribedusers_subscribed'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscribeduser',
            name='Suscribed',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
