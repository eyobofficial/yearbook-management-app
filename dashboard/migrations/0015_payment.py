# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-09 16:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_auto_20171009_1428'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Payment Title')),
                ('description', models.TextField(blank=True, help_text='Describe why this particular payment is needed', null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Payment Amount')),
                ('due_date', models.DateField(verbose_name='Due date of the payment')),
                ('publish', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['publish', 'due_date', 'amount'],
            },
        ),
    ]
