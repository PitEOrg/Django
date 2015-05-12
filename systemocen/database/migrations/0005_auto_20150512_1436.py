# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0004_message_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubGrade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=3)),
                ('date', models.DateTimeField()),
                ('grade_type', models.IntegerField(default=0)),
                ('student_id', models.ForeignKey(to='database.Student')),
            ],
        ),
        migrations.CreateModel(
            name='SubSubject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject_type', models.IntegerField(default=0)),
                ('subject_id', models.ForeignKey(to='database.Subject')),
                ('teacher_id', models.ForeignKey(to='database.Teacher')),
            ],
        ),
        migrations.RemoveField(
            model_name='grade',
            name='grade_type',
        ),
        migrations.AddField(
            model_name='subgrade',
            name='sub_subject_id',
            field=models.ForeignKey(to='database.SubSubject'),
        ),
        migrations.AddField(
            model_name='subgrade',
            name='teacher_id',
            field=models.ForeignKey(to='database.Teacher'),
        ),
    ]
