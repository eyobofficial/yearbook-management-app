# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-02 02:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20171001_1857'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentyearbook',
            name='photo',
            field=models.ImageField(default='uploads/no_photo.jpg', upload_to='uploads/'),
        ),
    ]