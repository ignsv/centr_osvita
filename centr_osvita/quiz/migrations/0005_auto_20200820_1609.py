# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-08-20 16:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_auto_20200820_1606'),
    ]

    def add_simple_test_param(apps, schema):
        TestParameter = apps.get_model('quiz', 'TestParameter')
        Test = apps.get_model('quiz', 'Test')

        for test in Test.objects.all():
            test.test_parameter = TestParameter.objects.create(
                number_of_common_questions=3,
                number_of_order_questions=3,
                number_of_mapping_questions=3,
                coefficient_of_common_question=1,
                coefficient_of_order_question=1,
                coefficient_of_mapping_question=1
            )
            test.save()

    def reverse_add_simple_test_param(apps, schema):
        pass

    operations = [
        migrations.RunPython(add_simple_test_param, reverse_code=reverse_add_simple_test_param),
        migrations.AlterField(
            model_name='test',
            name='test_parameter',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quiz.TestParameter', verbose_name='Test Parameter'),
        ),
    ]