# Generated by Django 5.0.4 on 2024-05-11 10:49

import django.db.models.deletion
import shortuuidfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autho', '0002_rename_created_on_user_created_at_and_more'),
        ('cooperative', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='created_on',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='updated_on',
            new_name='modified_at',
        ),
        migrations.RenameField(
            model_name='loan',
            old_name='created_on',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='loan',
            old_name='updated_on',
            new_name='modified_at',
        ),
        migrations.RenameField(
            model_name='personalguarantor',
            old_name='created_on',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='personalguarantor',
            old_name='updated_on',
            new_name='modified_at',
        ),
        migrations.RemoveField(
            model_name='company',
            name='if_profiter_then_no_shareholders',
        ),
        migrations.RemoveField(
            model_name='company',
            name='share_holders',
        ),
        migrations.RemoveField(
            model_name='loan',
            name='personal_guarantors',
        ),
        migrations.AddField(
            model_name='personalguarantor',
            name='loan',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='personal_guarantors', to='cooperative.loan'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='company',
            name='idx',
            field=shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22),
        ),
        migrations.AlterField(
            model_name='company',
            name='is_obsolete',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='loan',
            name='idx',
            field=shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22),
        ),
        migrations.AlterField(
            model_name='loan',
            name='is_obsolete',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.AlterField(
            model_name='personalguarantor',
            name='idx',
            field=shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22),
        ),
        migrations.AlterField(
            model_name='personalguarantor',
            name='is_obsolete',
            field=models.BooleanField(db_index=True, default=False),
        ),
        migrations.CreateModel(
            name='LoanApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idx', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_obsolete', models.BooleanField(db_index=True, default=False)),
                ('loan_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autho.user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Shareholder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idx', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_obsolete', models.BooleanField(db_index=True, default=False)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='share_holders', to='cooperative.company')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autho.user')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
