# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizext', '0007_auto_20151102_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='attempt',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
