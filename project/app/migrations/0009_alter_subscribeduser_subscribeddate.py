# Generated by Django 3.2.7 on 2021-12-03 06:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_alter_subscribeduser_subscribeddate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscribeduser',
            name='SubscribedDate',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
