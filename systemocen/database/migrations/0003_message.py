# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0002_student_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contents', models.CharField(max_length=400)),
                ('is_read', models.BooleanField()),
                ('student_id', models.ForeignKey(to='database.Student')),
                ('teacher_id', models.ForeignKey(to='database.Teacher')),
            ],
        ),
    ]
