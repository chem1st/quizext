# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizext', '0006_auto_20151023_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='attempt',
            name='current_q',
            field=models.PositiveIntegerField(default=1, verbose_name='\u0422\u0435\u043a\u0443\u0449\u0438\u0439 \u0432\u043e\u043f\u0440\u043e\u0441', blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attempt',
            name='question_list',
            field=models.CharField(max_length=1024, blank=True),
        ),
        migrations.AddField(
            model_name='question',
            name='answer',
            field=models.CharField(max_length=1024, verbose_name='\u041e\u0442\u0432\u0435\u0442', blank=True),
        ),
        migrations.AddField(
            model_name='test',
            name='fail_text',
            field=models.TextField(verbose_name='\u0422\u0435\u043a\u0441\u0442 \u0432 \u0441\u043b\u0443\u0447\u0430\u0435 \u043f\u0440\u043e\u0432\u0430\u043b\u0430', blank=True),
        ),
        migrations.AddField(
            model_name='test',
            name='success_text',
            field=models.TextField(verbose_name='\u0422\u0435\u043a\u0441\u0442 \u0432 \u0441\u043b\u0443\u0447\u0430\u0435 \u043f\u0440\u043e\u0445\u043e\u0436\u0434\u0435\u043d\u0438\u044f', blank=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(related_name='answers', to='quizext.Question'),
        ),
        migrations.AlterField(
            model_name='attempt',
            name='answers',
            field=models.CharField(max_length=1024, verbose_name='\u043e\u0442\u0432\u0435\u0442\u044b', blank=True),
        ),
    ]
