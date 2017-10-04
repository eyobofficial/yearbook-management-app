# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-03 19:58
from __future__ import unicode_literals

import dashboard.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_auto_20171002_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentyearbook',
            name='gown_photo',
            field=models.ImageField(default='/upload/no_photo.jpg', upload_to=dashboard.models.gown_photo_path, verbose_name='Gown Photo (Academic Dress)'),
        ),
    ]