# encoding: UTF-8
from django.db import models


class Test(models.Model):
	title = models.CharField(u"Название", max_length=150)
	description = models.TextField(u"Описание", blank=True)

	def __unicode__(self):
		return self.title

	class Meta:
		verbose_name = "Тест"
		verbose_name_plural = "Тесты"


class Question(models.Model):
	test = models.ForeignKey(Test, verbose_name="Тест")
	content = models.TextField(u"Текст вопроса")
	group = models.PositiveIntegerField(u"Серия")

	def __unicode__(self):
		return "%s" % self.content[:40]

	class Meta:
		verbose_name = "Вопрос"
		verbose_name_plural = "Вопросы"
		ordering = ['group', 'id']


class Answer(models.Model):
	question = models.ForeignKey(Question)
	content = models.CharField(u"Текст ответа", max_length=300)
	is_correct = models.BooleanField(u"Верно")

	def __unicode__(self):
		return "%s ..." % self.content[:20]

	class Meta:
		verbose_name = "Ответ"
		verbose_name_plural = "Ответы"
