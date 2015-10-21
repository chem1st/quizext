# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizext', '0004_auto_20151021_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attempt',
            name='points',
            field=models.PositiveIntegerField(null=True, verbose_name='\u041d\u0430\u0431\u0440\u0430\u043d\u043d\u044b\u0435 \u0431\u0430\u043b\u043b\u044b', blank=True),
        ),
    ]
