# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('quizext', '0009_auto_20151103_0207'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attempt',
            name='max_laps',
        ),
        migrations.AddField(
            model_name='test',
            name='max_laps',
            field=models.PositiveIntegerField(default=1, verbose_name='\u041c\u0430\u043a\u0441. \u043a\u043e\u043b\u0438\u0447\u0435\u0441\u0442\u0432\u043e \u043a\u0440\u0443\u0433\u043e\u0432'),
        ),
        migrations.AlterField(
            model_name='attempt',
            name='user',
            field=models.ForeignKey(verbose_name=b'\xd0\x9f\xd0\xbe\xd0\xbb\xd1\x8c\xd0\xb7\xd0\xbe\xd0\xb2\xd0\xb0\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8c', to=settings.AUTH_USER_MODEL),
        ),
    ]
