# Generated by Django 3.2.7 on 2021-12-07 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_alter_subscribeduser_subscribeddate'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscribeduser',
            name='Month',
            field=models.CharField(default=1, max_length=500),
            preserve_default=False,
        ),
    ]
