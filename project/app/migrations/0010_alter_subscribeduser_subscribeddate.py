# Generated by Django 3.2.7 on 2021-12-03 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_subscribeduser_subscribeddate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscribeduser',
            name='SubscribedDate',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]