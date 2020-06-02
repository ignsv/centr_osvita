# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-06-02 19:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0005_commonanswer_number'),
    ]

    def add_order_common_answers(apps, schema):
        CommonAnswer = apps.get_model('quiz', 'CommonAnswer')

        for answer in CommonAnswer.objects.all():
            answer.number = 1

    def reverse_add_order_common_answers(apps, schema):
        pass

    operations = [
        migrations.RunPython(add_order_common_answers, reverse_code=reverse_add_order_common_answers),
        migrations.AlterField(
            model_name='commonanswer',
            name='number',
            field=models.IntegerField(choices=[(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D')], verbose_name='Answer FIRST Position'),
        ),
    ]
