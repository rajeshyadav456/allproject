# Generated by Django 3.2.7 on 2021-11-16 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_delete_history'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='active',
            field=models.IntegerField(choices=[(0, 'Inactive'), (1, 'Active')], default=0),
        ),
    ]