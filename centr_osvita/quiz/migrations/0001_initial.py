# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-05-29 01:11
from __future__ import unicode_literals

import centr_osvita.quiz.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
            ],
            options={
                'verbose_name': 'Answer',
                'verbose_name_plural': 'Answers',
                'manager_inheritance_from_future': True,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('text', models.TextField(verbose_name='Text')),
                ('image', models.ImageField(blank=True, null=True, upload_to=centr_osvita.quiz.models.question_image_path, verbose_name='Image')),
                ('type', models.IntegerField(choices=[(0, 'common'), (1, 'order'), (2, 'mapping')], default=0, verbose_name='Question Type')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('name', models.CharField(help_text='Maximum length is 255 symbols', max_length=255, verbose_name='Subject name')),
                ('status', models.BooleanField(default=0, verbose_name='Publish status')),
            ],
            options={
                'verbose_name': 'Subject',
                'verbose_name_plural': 'Subjects',
            },
        ),
        migrations.CreateModel(
            name='CommonAnswer',
            fields=[
                ('answer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='quiz.Answer')),
                ('text', models.CharField(max_length=255, verbose_name='Text')),
                ('correct', models.BooleanField(default=0, verbose_name='Correct answer')),
            ],
            options={
                'verbose_name': 'Common Answer',
                'verbose_name_plural': 'Common Answers',
                'manager_inheritance_from_future': True,
            },
            bases=('quiz.answer',),
        ),
        migrations.CreateModel(
            name='MappingAnswer',
            fields=[
                ('answer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='quiz.Answer')),
                ('number_1', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (0, '0')], verbose_name='First chain')),
                ('number_2', models.IntegerField(choices=[(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D'), (5, 'E')], verbose_name='Second chain')),
                ('text_1', models.CharField(blank=True, max_length=255, null=True, verbose_name='Text 1')),
                ('text_2', models.CharField(max_length=255, verbose_name='Text 2')),
            ],
            options={
                'verbose_name': 'Mapping Answer',
                'verbose_name_plural': 'Mapping Answers',
                'manager_inheritance_from_future': True,
            },
            bases=('quiz.answer',),
        ),
        migrations.CreateModel(
            name='OrderAnswer',
            fields=[
                ('answer_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='quiz.Answer')),
                ('text', models.CharField(max_length=255, verbose_name='Text')),
                ('number', models.IntegerField(choices=[(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D')], verbose_name='Answer Position')),
            ],
            options={
                'verbose_name': 'Order Answer',
                'verbose_name_plural': 'Order Answers',
                'manager_inheritance_from_future': True,
            },
            bases=('quiz.answer',),
        ),
        migrations.AddField(
            model_name='question',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='quiz.Subject', verbose_name='Subject'),
        ),
        migrations.AddField(
            model_name='answer',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_quiz.answer_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=centr_osvita.quiz.models.NON_POLYMORPHIC_CASCADE, related_name='answers', to='quiz.Question', verbose_name='Question'),
        ),
    ]
