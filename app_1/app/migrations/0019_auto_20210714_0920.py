# Generated by Django 3.2.4 on 2021-07-14 09:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0018_guests'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='Likes',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='items',
            name='TimesPlayed',
            field=models.BigIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='UserPreviouslyPlayed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item55', to='app.items')),
                ('User_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user35', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GuestPreviouslyPlayed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Guest_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user45', to='app.guests')),
                ('Item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item85', to='app.items')),
            ],
        ),
    ]