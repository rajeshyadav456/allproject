# Generated by Django 3.2.7 on 2022-04-04 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0024_auto_20220404_0921'),
    ]

    operations = [
        migrations.AddField(
            model_name='hostmatches',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='hostmatches',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
