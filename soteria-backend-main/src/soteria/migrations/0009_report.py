# Generated by Django 4.0.5 on 2022-11-22 05:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('soteria', '0008_userorganization'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, verbose_name='last updated at')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='name')),
                ('column_mapping', models.JSONField()),
                ('included_columns', models.JSONField()),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='soteria.organization')),
            ],
            options={
                'db_table': 'soteria_report',
            },
        ),
    ]
