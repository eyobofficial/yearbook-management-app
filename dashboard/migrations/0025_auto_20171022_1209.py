# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-22 09:09
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0024_auto_20171021_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentyearbook',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
