# Generated by Django 5.0.4 on 2024-04-20 13:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('autho', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idx', models.UUIDField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('is_obsolete', models.BooleanField(db_index=True, default=True)),
                ('name', models.CharField(max_length=255)),
                ('pan_num', models.CharField(blank=True, max_length=9, null=True)),
                ('vat_num', models.CharField(blank=True, max_length=9, null=True)),
                ('permanent_add', models.CharField(max_length=255)),
                ('pan_registration_date', models.DateField(blank=True, null=True)),
                ('pan_registration_place', models.CharField(blank=True, max_length=100, null=True)),
                ('if_profiter_then_no_shareholders', models.CharField(blank=True, max_length=100, null=True)),
                ('lone_taker_type', models.CharField(choices=[('personal', 'Personal'), ('company', 'Company')], default='company', max_length=10)),
                ('profiter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='autho.user')),
                ('share_holders', models.ManyToManyField(blank=True, related_name='companies', to='autho.user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PersonalGuarantor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idx', models.UUIDField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('is_obsolete', models.BooleanField(db_index=True, default=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='autho.user')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Loan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idx', models.UUIDField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('is_obsolete', models.BooleanField(db_index=True, default=True)),
                ('name', models.CharField(max_length=100)),
                ('nature', models.CharField(choices=[('term', 'Term'), ('overdraft', 'Overdraft (OD)')], default='term', max_length=25)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('maturity_date', models.DateField()),
                ('installment_due_type', models.CharField(choices=[('d', 'Daily'), ('m', 'Monthly'), ('q', 'Quarterly'), ('y', 'Yearly')], default='d', max_length=1)),
                ('emi_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('currently_outstanding', models.DecimalField(decimal_places=2, max_digits=12)),
                ('total_due', models.DecimalField(decimal_places=2, max_digits=12)),
                ('personal_guarantors', models.ManyToManyField(blank=True, related_name='guaranted_loans', to='cooperative.personalguarantor')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
