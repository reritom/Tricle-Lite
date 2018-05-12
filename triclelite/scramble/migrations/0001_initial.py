# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-05-12 11:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveURL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(default=0, max_length=255, unique=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('expired', models.BooleanField(default=False)),
                ('processed', models.BooleanField(default=False)),
                ('number_of_files', models.IntegerField(default=0)),
                ('mode', models.CharField(default='Scramble', max_length=255)),
                ('down_count', models.IntegerField(default=0)),
                ('sessionToken', models.CharField(default=0, max_length=255)),
                ('start', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('end', models.DateTimeField(default=django.utils.timezone.now, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExpiredURL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(default=0, max_length=255, unique=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('number_of_files', models.IntegerField(default=0)),
                ('mode', models.CharField(default='Scramble', max_length=255)),
                ('duration', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ImageDataStore',
            fields=[
                ('id', models.CharField(default='8dc2588b8f7d4a0c8dd67d4d1f1d167d', max_length=255, primary_key=True, serialize=False)),
                ('file_type', models.CharField(default=0, max_length=255)),
                ('file_size', models.IntegerField(default=0)),
                ('file_name', models.CharField(default=0, max_length=255)),
                ('related_url', models.CharField(default=0, max_length=255)),
                ('mode', models.CharField(default=0, max_length=255)),
                ('process_time', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='UrlItem',
            fields=[
                ('id', models.CharField(default='0f3ca16a2cb9423a9bd7f2e6083d1505', max_length=255, primary_key=True, serialize=False)),
                ('file_name', models.CharField(default=0, max_length=255)),
                ('file_type', models.CharField(default=0, max_length=255)),
                ('file_size', models.IntegerField(default=0)),
                ('processed', models.BooleanField(default=False)),
                ('process_start', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('process_end', models.DateTimeField(default=django.utils.timezone.now, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='KeyChain',
            fields=[
                ('active', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='scramble.ActiveURL')),
                ('key_one', models.CharField(default=0, max_length=255)),
                ('key_two', models.CharField(default=0, max_length=255)),
                ('key_three', models.CharField(default=0, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ZipLock',
            fields=[
                ('active', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='scramble.ActiveURL')),
                ('zipcode', models.CharField(default=0, max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='urlitem',
            name='active',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='scramble.ActiveURL'),
        ),
    ]
