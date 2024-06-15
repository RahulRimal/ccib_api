# Generated by Django 5.0.4 on 2024-06-07 16:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autho', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staffuser',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='staffuser',
            name='id',
        ),
        migrations.RemoveField(
            model_name='staffuser',
            name='idx',
        ),
        migrations.RemoveField(
            model_name='staffuser',
            name='is_obsolete',
        ),
        migrations.RemoveField(
            model_name='staffuser',
            name='modified_at',
        ),
        migrations.RemoveField(
            model_name='staffuser',
            name='user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_staff',
        ),
        migrations.AddField(
            model_name='staffuser',
            name='is_active',
            field=models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active'),
        ),
        migrations.AddField(
            model_name='staffuser',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status'),
        ),
        migrations.AddField(
            model_name='staffuser',
            name='user_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='autho.user'),
            preserve_default=False,
        ),
    ]
