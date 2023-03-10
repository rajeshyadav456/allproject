# Generated by Django 3.2.4 on 2021-07-05 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_profile_profile_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profilemodel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_img', models.ImageField(upload_to=None)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('phonenumber', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'Profile',
            },
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
