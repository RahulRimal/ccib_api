# Generated by Django 5.0.4 on 2024-05-12 10:52

import shortuuidfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooperative', '0002_rename_created_on_company_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Finance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idx', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_obsolete', models.BooleanField(db_index=True, default=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1000)),
                ('location', models.JSONField(default=dict)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]