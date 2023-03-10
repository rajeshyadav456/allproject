# Generated by Django 3.2.4 on 2021-09-07 04:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0040_auto_20210901_0613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usernotifications',
            name='DateAdded',
            field=models.DateTimeField(default='2021 58 09/07/21 - 04:58:57'),
        ),
        migrations.CreateModel(
            name='Favourites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DateAdded', models.DateTimeField(default=django.utils.timezone.now)),
                ('Item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='item121', to='app.items')),
                ('User_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user321', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]