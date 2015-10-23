# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizext', '0005_auto_20151021_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='attempt',
            name='endtime',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='attempt',
            name='starttime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='attempt',
            name='timetill',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
