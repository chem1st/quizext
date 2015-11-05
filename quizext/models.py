# encoding: UTF-8
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
import datetime
import json


class Test(models.Model):
	title = models.CharField(u"Название", max_length=150)
	description = models.TextField(u"Описание", blank=True)
	user = models.ManyToManyField(User, through='Attempt')
	max_attempts = models.PositiveIntegerField(u'Кол-во попыток', blank=True)
	max_laps = models.PositiveIntegerField(u'Макс. количество кругов', default=1)
	time = models.FloatField(u'Продолжительность, сек', blank=True)
	success_text = models.TextField(u"Текст в случае прохождения", blank=True)
	fail_text = models.TextField(u"Текст в случае провала", blank=True)

	class Meta:
		verbose_name = "Тест"
		verbose_name_plural = "Тесты"

	def __unicode__(self):
		return self.title

	def count_questions(self):
		return self.question_set.values('group').distinct().count()

	def max_points(self):
		return self.question_set.values('group').distinct().aggregate(Sum('points')).values()[0]

	def time_limit(self):
		return self.time/3600


class Question(models.Model):
	test = models.ForeignKey(Test, verbose_name="Тест")
	content = models.TextField(u"Текст вопроса")
	group = models.PositiveIntegerField(u"Серия")
	points = models.PositiveIntegerField(u'Баллы')
	img = models.ImageField(blank=False)
	is_free = models.BooleanField(u'Свободный ответ', default=False)

	class Meta:
		verbose_name = "Вопрос"
		verbose_name_plural = "Вопросы"
		ordering = ['group', 'id']

	def __unicode__(self):
		return self.content[:47] + '...' if len(self.content) > 50 else self.content


class Answer(models.Model):
	question = models.ForeignKey(Question, related_name='answers')
	content = models.CharField(u"Текст ответа", max_length=300)
	is_correct = models.BooleanField(u"Верно", default=False)

	class Meta:
		verbose_name = "Вариант ответа"
		verbose_name_plural = "Варианты ответов"

	def __unicode__(self):
		return self.content


class Attempt(models.Model):
	user = models.ForeignKey(User, verbose_name="Пользователь")
	test = models.ForeignKey(Test, verbose_name="Тест")
	number = models.PositiveIntegerField(u'Номер попытки')
	lap = models.PositiveIntegerField(u'Круг', default=1)
	question_list = models.CharField(max_length=1024, blank=True)
	skipped_list = models.CharField(max_length=1024, blank=True)
	answers = models.CharField(u'ответы', max_length=1024, blank=True)
	current_q = models.PositiveIntegerField(u'Текущий вопрос', blank=True)
	points = models.PositiveIntegerField(u'Набранные баллы', default=0)
	starttime = models.DateTimeField(auto_now_add=True, null=True)
	is_active = models.BooleanField(default=False)
	endtime = models.DateTimeField(blank=True, null=True)
	timetill = models.DateTimeField(blank=True, null=True)

	def __unicode__(self):
		return u"%s - %s (попытка №%s)" % (self.test.title, self.user.username, self.number)

	def set_json(self, x):
		self.answers = json.dumps(x)

	def get_json(self):
		try:
			return json.loads(self.answers)
		except:
			return {}

	def current_question(self):
		if self.lap < 2:
			question_list = json.loads(self.question_list)
		else:
			question_list = json.loads(self.skipped_list)
		question_id = question_list[self.current_q-1]
		return Question.objects.get(id=question_id)

	def next_question(self):
		self.current_q += 1
		self.save()

	def add_skipped_question(self):
		try:
			skipped_list = json.loads(self.skipped_list)
		except:
			skipped_list = []
		q = self.current_question()
		if not q.id in skipped_list:
			skipped_list.append(q.id)
			self.skipped_list = json.dumps(skipped_list)

	def rm_skipped_question(self, q):
		try:
			skipped_list = json.loads(self.skipped_list)
			if q.id in skipped_list:
				skipped_list.remove(q.id)
				self.skipped_list = json.dumps(skipped_list)
				self.current_q -= 1
		except:
			pass

	def add_answered_question(self, answered):
		q = self.current_question()
		self.rm_skipped_question(q)
		answers = self.get_json()
		if q.is_free:
			correct = Answer.objects.get(question__id=q.id, 
				is_correct=True).content
			if int(correct) == int(answered):
				self.points += int(q.points)
			answers[q.id] = ['f', answered]
		else:	
			correct = Answer.objects.filter(question__id=q.id, 
				is_correct=True).values_list('id', flat=True)
			answered = [answer.pk for answer in answered]
			if map(int, correct) == map(int, answered):
				self.points += int(q.points)
			answers[q.id] = answered
		self.set_json(answers)

	def count_answered(self):
		answers = self.get_json()
		answered = 0
		for k in answers.keys():
			if answers[k]:
				answered += 1
		return answered 

	def close(self):
		self.is_active=False
		self.endtime = datetime.datetime.now()
		self.save()

	def next_lap(self):
		try:
			skipped_list = json.loads(self.skipped_list)
		except:
			return False
		if self.lap < self.test.max_laps and skipped_list:
			self.lap += 1
			self.current_q = 1
			self.save()
			return self.current_question()
		else:
			return False

	def save(self, *args, **kwargs):
		if not self.id:
			self.is_active=True
			self.timetill = datetime.datetime.now() + datetime.timedelta(seconds=self.test.time)
			question_list = []
			current_test_q = Question.objects.filter(test__pk=self.test.pk)
			group_overall = current_test_q.values('group').distinct().count() + 1
			for q_set in range(1, group_overall):
				q = current_test_q.filter(group=q_set).order_by('?').first()
				question_list.append(q.id)
			self.question_list = json.dumps(question_list)
			self.current_q = 1

		return super(Attempt, self).save(*args, **kwargs)
