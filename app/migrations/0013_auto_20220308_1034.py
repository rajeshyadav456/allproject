# Generated by Django 3.0 on 2022-03-08 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20220308_0928'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profiles',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='profiles',
            name='longitude',
        ),
    ]
