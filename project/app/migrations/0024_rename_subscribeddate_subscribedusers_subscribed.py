# Generated by Django 3.2.7 on 2021-12-10 10:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0023_auto_20211210_0937'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subscribedusers',
            old_name='SubscribedDate',
            new_name='Subscribed',
        ),
    ]
