# Generated by Django 3.1.7 on 2021-06-22 22:30

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name')),
                ('stars', models.PositiveSmallIntegerField(default=0, verbose_name='Stars')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
            ],
            options={
                'verbose_name': 'Hotel',
                'verbose_name_plural': 'Hotels',
                'ordering': ('-stars', 'name'),
            },
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_type', models.PositiveSmallIntegerField(choices=[(1, 'Regular'), (2, 'Reward')], verbose_name='Type Client')),
                ('day', models.CharField(choices=[('mon', 'Monday'), ('tues', 'Tuesday'), ('wed', 'Wednesday'), ('thur', 'Thursday'), ('fri', 'Friday'), ('sat', 'Saturday'), ('sun', 'Sunday')], max_length=4, verbose_name='Day')),
                ('value', models.FloatField(verbose_name='Value')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.hotel', verbose_name='Hotel Tax')),
            ],
            options={
                'verbose_name': 'Client',
                'verbose_name_plural': 'Clients',
                'ordering': ('hotel', 'client_type', 'day'),
            },
        ),
        migrations.CreateModel(
            name='Reserve',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('telefone', models.CharField(max_length=11, validators=[django.core.validators.MinValueValidator(11)], verbose_name='Telefone')),
                ('start', models.DateField(verbose_name='Entrance')),
                ('end', models.DateField(verbose_name='Exit')),
                ('value', models.FloatField(verbose_name='Value of reserve')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.hotel', verbose_name='Hotel')),
            ],
            options={
                'verbose_name': 'Reserve',
                'verbose_name_plural': 'Reserves',
                'ordering': ('hotel', 'name'),
            },
        ),
    ]
