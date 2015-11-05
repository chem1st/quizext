# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizext', '0010_auto_20151104_0357'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='answer',
        ),
        migrations.AddField(
            model_name='question',
            name='is_free',
            field=models.BooleanField(default=False, verbose_name='\u0421\u0432\u043e\u0431\u043e\u0434\u043d\u044b\u0439 \u043e\u0442\u0432\u0435\u0442'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='is_correct',
            field=models.BooleanField(default=False, verbose_name='\u0412\u0435\u0440\u043d\u043e'),
        ),
    ]
