# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-07-10 14:03
from __future__ import unicode_literals

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_auto_20200710_1358'),
    ]

    def change_altered_fields(apps, schema):
        Profile = apps.get_model('profiles', 'Profile')

        for profile in Profile.objects.all():
            profile.institution_name = 'OXFORD'
            profile.parent_full_name = 'JOHN DOE'
            profile.parent_phone = '+41524204242'
            profile.save()

    def reverse_change_altered_fields(apps, schema):
        pass

    operations = [
        migrations.RunPython(change_altered_fields, reverse_code=reverse_change_altered_fields),
        migrations.AlterField(
            model_name='profile',
            name='institution_name',
            field=models.CharField(help_text='Maximum length is 255 symbols', max_length=255, verbose_name='Institution name'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='parent_full_name',
            field=models.CharField(help_text='Maximum length is 255 symbols', max_length=255, verbose_name='Parent fullname'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='parent_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, verbose_name='Parent phone'),
        ),
    ]
