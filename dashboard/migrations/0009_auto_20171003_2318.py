# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-03 20:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0008_auto_20171003_2258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentyearbook',
            name='birthdate',
            field=models.DateField(help_text='Use YYYY-MM-DD format. Example: 1999-09-26'),
        ),
    ]