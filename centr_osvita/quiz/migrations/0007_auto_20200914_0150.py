# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-09-13 22:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_auto_20200828_2212'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='testparameter',
            options={'verbose_name': 'Test Parameter', 'verbose_name_plural': 'Test Parameters'},
        ),
        migrations.AlterModelOptions(
            name='year',
            options={'verbose_name': 'Year', 'verbose_name_plural': 'Years'},
        ),
        migrations.AlterModelOptions(
            name='yearsubjectstatistics',
            options={'verbose_name': 'Year Subject Statisctic', 'verbose_name_plural': 'Year Subject Statisctics'},
        ),
    ]
