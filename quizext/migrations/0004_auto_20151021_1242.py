# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizext', '0003_auto_20151019_2110'),
    ]

    operations = [
        migrations.AddField(
            model_name='attempt',
            name='points',
            field=models.PositiveIntegerField(default=1, verbose_name='\u041d\u0430\u0431\u0440\u0430\u043d\u043d\u044b\u0435 \u0431\u0430\u043b\u043b\u044b'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attempt',
            name='answers',
            field=models.CharField(max_length=1000, verbose_name='\u043e\u0442\u0432\u0435\u0442\u044b', blank=True),
        ),
    ]
