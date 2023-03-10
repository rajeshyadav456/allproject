# Generated by Django 3.2.7 on 2021-12-06 06:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_remove_subscribeduser_month'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('total', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='subscribeduser',
            name='SubscribedDate',
        ),
        migrations.AddField(
            model_name='subscribeduser',
            name='Date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
