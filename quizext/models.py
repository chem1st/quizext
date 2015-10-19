# encoding: UTF-8
from django.db import models
from django.contrib.auth.models import User
import json


class Test(models.Model):
	title = models.CharField(u"Название", max_length=150)
	description = models.TextField(u"Описание", blank=True)
	user = models.ManyToManyField(User, through='Attempt')
	max_attempts = models.PositiveIntegerField(u'Кол-во попыток', blank=True)
	time = models.FloatField(u'Продолжительность, сек', blank=True)

	def __unicode__(self):
		return self.title

	class Meta:
		verbose_name = "Тест"
		verbose_name_plural = "Тесты"


class Question(models.Model):
	test = models.ForeignKey(Test, verbose_name="Тест")
	content = models.TextField(u"Текст вопроса")
	group = models.PositiveIntegerField(u"Серия")
	points = models.PositiveIntegerField(u'Баллы')

	def __unicode__(self):
		return self.content[:47] + '...' if len(self.content) > 50 else self.content

	class Meta:
		verbose_name = "Вопрос"
		verbose_name_plural = "Вопросы"
		ordering = ['group', 'id']


class Answer(models.Model):
	question = models.ForeignKey(Question)
	content = models.CharField(u"Текст ответа", max_length=300)
	is_correct = models.BooleanField(u"Верно")

	def __unicode__(self):
		return self.content[:27] + '...' if len(self.content) > 30 else self.content

	class Meta:
		verbose_name = "Вариант ответа"
		verbose_name_plural = "Варианты ответов"


class Attempt(models.Model):
	user = models.ForeignKey(User, verbose_name="Пользователь")
	test = models.ForeignKey(Test, verbose_name="Тест")
	number = models.PositiveIntegerField(u'Номер попытки')
	questions = models.CharField(u'Вопросы', max_length=500)
	checked = models.CharField(u'Ответы', max_length=500)

	def set_json(self, field, x):
		self.field = json.dumps(x)

	def get_json(self, field, x):
		return json.loads(self.field)

	def __unicode__(self):
		return "%s - %s (%s)" % (self.test, self.user, self.number)
