# encoding: UTF-8
from django.db import models
from django.contrib.auth.models import User
import datetime
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
	answers = models.CharField(u'ответы', max_length=1000, blank=True)
	points = models.PositiveIntegerField(u'Набранные баллы', blank=True, null=True)
	starttime = models.DateTimeField(auto_now_add=True, null=True)
	endtime = models.DateTimeField(blank=True, null=True)
	timetill = models.DateTimeField(blank=True, null=True)

	def __unicode__(self):
		return u"%s - %s (попытка №%s)" % (self.test.title, self.user.username, self.number)

	def set_json(self, x):
		self.answers = json.dumps(x)

	def get_json(self):
		return json.loads(self.answers)

	def save(self, *args, **kwargs):
		if not self.id:
			self.timetill = datetime.datetime.now() + datetime.timedelta(seconds=self.test.time)
		return super(Attempt, self).save(*args, **kwargs)