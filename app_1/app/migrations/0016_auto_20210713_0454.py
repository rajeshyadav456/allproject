# Generated by Django 3.2.4 on 2021-07-13 04:54

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0015_rename_comments_comments_comment'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RequestAudio',
            new_name='RequestedAudio',
        ),
        migrations.RenameField(
            model_name='categories',
            old_name='Category',
            new_name='Name',
        ),
        migrations.RemoveField(
            model_name='seasons',
            name='NumberOfSeasons',
        ),
        migrations.AddField(
            model_name='categories',
            name='PosterImage',
            field=models.ImageField(blank=True, null=True, upload_to='CategoryImages'),
        ),
        migrations.AddField(
            model_name='episodes',
            name='PosterImage',
            field=models.ImageField(blank=True, null=True, upload_to='EpisodeImages'),
        ),
        migrations.AddField(
            model_name='items',
            name='PosterImage',
            field=models.ImageField(blank=True, null=True, upload_to='ItemImages'),
        ),
        migrations.AddField(
            model_name='seasons',
            name='PosterImage',
            field=models.ImageField(blank=True, null=True, upload_to='SeasonImages'),
        ),
        migrations.AddField(
            model_name='seasons',
            name='SeasonName',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
