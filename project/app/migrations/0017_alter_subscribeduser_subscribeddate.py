# Generated by Django 3.2.7 on 2021-12-10 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0016_city_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscribeduser',
            name='SubscribedDate',
            field=models.DateField(auto_now_add=True),
        ),
    ]
