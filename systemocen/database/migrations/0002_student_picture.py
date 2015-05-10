# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='picture',
            field=models.ImageField(upload_to=b'profile_images', blank=True),
        ),
    ]
