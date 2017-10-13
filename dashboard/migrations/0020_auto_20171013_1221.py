# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-13 09:21
from __future__ import unicode_literals

import dashboard.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0019_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_photo',
            field=models.ImageField(default='defaults/default_profile_photo.jpg', upload_to=dashboard.models.profile_photo_path),
        ),
    ]
