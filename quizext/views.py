# encoding: UTF-8
from django.db.models import Sum, Max
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.core.urlresolvers import reverse
from .models import Test, Question, Answer, Attempt
from .forms import QuestionForm
import json


class TestList(ListView):
	model = Test
	context_object_name = 'tests'
	template_name = 'quizext/tests.html'


class TestDetail(DetailView):
	model = Test
	context_object_name = 'test'
	template_name = 'quizext/test_confirm.html'

	def get_context_data(self, **kwargs):
		context = super(TestDetail, self).get_context_data(**kwargs)
		q = Question.objects.filter(test__pk=self.kwargs['pk'])
		context['q_count'] = q.values('group').distinct().count()
		context['sum'] = q.aggregate(Sum('points')).values()[0]
		context['time'] = Test.objects.filter(pk=self.kwargs['pk']).values_list('time', 
			flat=True)[0]/3600
		user_attempts = Attempt.objects.filter(user=self.request.user, 
			test__pk=self.kwargs['pk']).count()
		max_attempts = Test.objects.get(pk=self.kwargs['pk']).max_attempts
		context['user_attempts'] = user_attempts
		context['delta_attempts'] = max_attempts - user_attempts
		context['user_max_points'] = Attempt.objects.filter(user=self.request.user, 
			test__pk=self.kwargs['pk']).aggregate(Max('points')).values()[0]
		return context

def startquiz(request, pk):
	attempt_count = Attempt.objects.filter(user=request.user, test__pk=pk).count() + 1
	test = Test.objects.get(pk=pk)
	attempt = Attempt(user=request.user, test=test, number=attempt_count)
	attempt.save()
	return HttpResponseRedirect(reverse('question', kwargs={'pk': pk, 'q_set': 1, 'attempt_count': attempt_count}))

def question(request, pk, q_set, attempt_count):
	try:
		q = Question.objects.filter(test__pk=pk).filter(group=q_set).order_by('?').first()
		next_q_set = Question.objects.filter(group__gt=q_set).order_by('group').first().group
	except:
		next_q_set = 0
	if request.method == "POST":
		attempt = Attempt.objects.get(user=request.user, test__pk=pk, number=attempt_count)
		correct = Answer.objects.filter(question__pk=request.POST.get('q_pk'), 
			is_correct=True).values_list('id', flat=True)
		checked = request.POST.getlist('answer')
		q_num = request.POST.get('q_pk')
		points = 0
		if map(int, correct) == map(int, checked):
			points = Question.objects.get(pk=q_num).points
		checked = [checked, points]
		try:
			answers = attempt.get_json()
		except ValueError:
			answers = {}
		answers[q_num] = checked
		attempt.set_json(answers)
		attempt.save()
		if int(q_set) == 0:
			return HttpResponseRedirect(reverse('results', kwargs={'pk': pk, 'attempt_count': attempt_count}))
		c = {'question': q, 'next': next_q_set, 'attempt_count': attempt_count, 'answers': answers}
	c = {'question': q, 'next': next_q_set, 'attempt_count': attempt_count}
	return render(request, 'quizext/question.html', c)


def results(request, pk, attempt_count):
	attempt = Attempt.objects.get(user=request.user, test__pk=pk, number=attempt_count)
	q = Question.objects.filter(test__pk=pk)
	q_count = q.values('group').distinct().count()
	p_sum = q.aggregate(Sum('points')).values()[0]
	user_points = 0
	try:
		answers = attempt.get_json()
		for k,kv in answers.iteritems():
			user_points += kv[1]
	except ValueError:
		pass
	attempt.points = user_points
	attempt.set_json(answers)
	attempt.save()
	user_percent = int(user_points) / int(p_sum) * 100
	c = {'test_title': attempt.test.title, 'answers': answers, 'q_count': q_count, 'p_sum': p_sum, 'user_points': user_points, 
		'user_percent': user_percent}
	return render(request, 'quizext/results.html', c)
