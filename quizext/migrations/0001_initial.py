# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=300, verbose_name='\u0422\u0435\u043a\u0441\u0442 \u043e\u0442\u0432\u0435\u0442\u0430')),
                ('is_correct', models.BooleanField(verbose_name='\u0412\u0435\u0440\u043d\u043e')),
            ],
            options={
                'verbose_name': '\u0412\u0430\u0440\u0438\u0430\u043d\u0442 \u043e\u0442\u0432\u0435\u0442\u0430',
                'verbose_name_plural': '\u0412\u0430\u0440\u0438\u0430\u043d\u0442\u044b \u043e\u0442\u0432\u0435\u0442\u043e\u0432',
            },
        ),
        migrations.CreateModel(
            name='Attempt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.PositiveIntegerField(verbose_name='\u041d\u043e\u043c\u0435\u0440 \u043f\u043e\u043f\u044b\u0442\u043a\u0438')),
                ('questions', models.CharField(max_length=500, verbose_name='\u0412\u043e\u043f\u0440\u043e\u0441\u044b')),
                ('checked', models.CharField(max_length=500, verbose_name='\u041e\u0442\u0432\u0435\u0442\u044b')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField(verbose_name='\u0422\u0435\u043a\u0441\u0442 \u0432\u043e\u043f\u0440\u043e\u0441\u0430')),
                ('group', models.PositiveIntegerField(verbose_name='\u0421\u0435\u0440\u0438\u044f')),
                ('points', models.PositiveIntegerField(verbose_name='\u0411\u0430\u043b\u043b\u044b')),
            ],
            options={
                'ordering': ['group', 'id'],
                'verbose_name': '\u0412\u043e\u043f\u0440\u043e\u0441',
                'verbose_name_plural': '\u0412\u043e\u043f\u0440\u043e\u0441\u044b',
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=150, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('description', models.TextField(verbose_name='\u041e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('max_attempts', models.PositiveIntegerField(verbose_name='\u041a\u043e\u043b-\u0432\u043e \u043f\u043e\u043f\u044b\u0442\u043e\u043a', blank=True)),
                ('time', models.FloatField(verbose_name='\u041f\u0440\u043e\u0434\u043e\u043b\u0436\u0438\u0442\u0435\u043b\u044c\u043d\u043e\u0441\u0442\u044c, \u0441\u0435\u043a', blank=True)),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='quizext.Attempt')),
            ],
            options={
                'verbose_name': '\u0422\u0435\u0441\u0442',
                'verbose_name_plural': '\u0422\u0435\u0441\u0442\u044b',
            },
        ),
        migrations.AddField(
            model_name='question',
            name='test',
            field=models.ForeignKey(verbose_name=b'\xd0\xa2\xd0\xb5\xd1\x81\xd1\x82', to='quizext.Test'),
        ),
        migrations.AddField(
            model_name='attempt',
            name='test',
            field=models.ForeignKey(verbose_name=b'\xd0\xa2\xd0\xb5\xd1\x81\xd1\x82', to='quizext.Test'),
        ),
        migrations.AddField(
            model_name='attempt',
            name='user',
            field=models.ForeignKey(verbose_name=b'\xd0\x9f\xd0\xbe\xd0\xbb\xd1\x8c\xd0\xb7\xd0\xbe\xd0\xb2\xd0\xb0\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8c', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(related_name='question', to='quizext.Question'),
        ),
    ]
