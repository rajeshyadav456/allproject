# Generated by Django 3.2.4 on 2021-09-01 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0039_auto_20210825_0725'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='requestedaudio',
            name='Category_id',
        ),
        migrations.AddField(
            model_name='requestedaudio',
            name='CategoryName',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='usernotifications',
            name='DateAdded',
            field=models.DateTimeField(default='2021 13 09/01/21 - 06:13:13'),
        ),
    ]
