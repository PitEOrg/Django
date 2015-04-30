# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=3)),
                ('date', models.DateTimeField()),
                ('grade_type', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectsStudents',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('student_id', models.ForeignKey(to='database.Student')),
                ('subject_id', models.ForeignKey(to='database.Subject')),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='subject',
            name='teacher_id',
            field=models.ForeignKey(to='database.Teacher'),
        ),
        migrations.AddField(
            model_name='grade',
            name='student_id',
            field=models.ForeignKey(to='database.Student'),
        ),
        migrations.AddField(
            model_name='grade',
            name='subject_id',
            field=models.ForeignKey(to='database.Subject'),
        ),
        migrations.AddField(
            model_name='grade',
            name='teacher_id',
            field=models.ForeignKey(to='database.Teacher'),
        ),
    ]
