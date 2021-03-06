# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-13 08:24
from __future__ import unicode_literals

import dashboard.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dashboard', '0018_auto_20171012_2100'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_photo', models.ImageField(default='uploads/no_photo.jpg', upload_to=dashboard.models.profile_photo_path)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
