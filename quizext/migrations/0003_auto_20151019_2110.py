# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizext', '0002_auto_20151019_1221'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attempt',
            name='checked',
        ),
        migrations.RemoveField(
            model_name='attempt',
            name='questions',
        ),
        migrations.AddField(
            model_name='attempt',
            name='answers',
            field=models.CharField(default=1, max_length=1000, verbose_name='\u043e\u0442\u0432\u0435\u0442\u044b'),
            preserve_default=False,
        ),
    ]
