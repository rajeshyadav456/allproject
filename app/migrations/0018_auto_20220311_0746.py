# Generated by Django 3.0 on 2022-03-11 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20220311_0604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessmodel',
            name='latitude',
            field=models.FloatField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='businessmodel',
            name='longitude',
            field=models.FloatField(blank=True, max_length=500, null=True),
        ),
    ]
