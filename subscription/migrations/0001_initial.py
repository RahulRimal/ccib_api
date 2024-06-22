# Generated by Django 5.0.4 on 2024-06-15 14:57

import django.db.models.deletion
import shortuuidfield.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cooperative', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idx', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_obsolete', models.BooleanField(db_index=True, default=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('period', models.CharField(choices=[('monthly', 'Monthly'), ('yearly', 'Yearly'), ('once', 'Once')], default='yearly', max_length=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idx', shortuuidfield.fields.ShortUUIDField(blank=True, editable=False, max_length=22)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_obsolete', models.BooleanField(db_index=True, default=False)),
                ('billing_start', models.DateField()),
                ('billing_end', models.DateField()),
                ('last_bill_paid', models.DateField()),
                ('next_billing', models.DateField()),
                ('grace_period', models.PositiveIntegerField(default=0)),
                ('status', models.CharField(choices=[('active', 'Active'), ('cancelled', 'Cancelled'), ('due', 'Due')], default='due', max_length=10)),
                ('is_payment_verified', models.BooleanField(default=False)),
                ('is_auto_renewable', models.BooleanField(default=True)),
                ('recurrance_period', models.DateField(blank=True, null=True)),
                ('finance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cooperative.finance')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='subscription.plan')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
