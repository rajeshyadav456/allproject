# Generated by Django 3.2.4 on 2021-07-23 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0031_auto_20210723_0914'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='ProfileImage',
            field=models.ImageField(blank=True, null=True, upload_to='media/UserProfileImages'),
        ),
        migrations.AlterField(
            model_name='usernotifications',
            name='DateAdded',
            field=models.DateTimeField(default='2021 16 07/23/21 - 09:16:43'),
        ),
    ]
