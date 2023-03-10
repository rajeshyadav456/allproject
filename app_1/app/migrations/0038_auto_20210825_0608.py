# Generated by Django 3.2.4 on 2021-08-25 06:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0037_auto_20210803_1716'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usernotifications',
            name='DateAdded',
            field=models.DateTimeField(default='2021 08 08/25/21 - 06:08:33'),
        ),
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Transaction_id', models.CharField(blank=True, max_length=500, null=True)),
                ('Amount', models.FloatField(blank=True, default=0, null=True)),
                ('Timeframe', models.CharField(blank=True, max_length=500, null=True)),
                ('DateAdded', models.DateTimeField(default=django.utils.timezone.now)),
                ('User_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user76', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
