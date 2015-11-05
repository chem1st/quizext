# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizext', '0011_auto_20151105_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='img',
            field=models.ImageField(default=1, upload_to=b''),
            preserve_default=False,
        ),
    ]
