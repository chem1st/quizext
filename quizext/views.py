# encoding: UTF-8
from django.db.models import Max, Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.core.urlresolvers import reverse
from .models import Test, Question, Answer, Attempt
from .forms import AnswerForm
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
		test = Test.objects.get(pk=self.kwargs['pk'])
		attempts = Attempt.objects.filter(user=self.request.user, 
			test__pk=self.kwargs['pk'])
		context['q_count'] = test.count_questions()
		context['sum'] = test.max_points()
		context['time'] = test.time_limit()
		user_attempts = attempts.count()
		max_attempts = test.max_attempts
		try:
			context['active_attempt'] = attempts.get(is_active=True)
		except:
			context['active_attempt'] = None
		context['user_attempts'] = user_attempts
		context['delta_attempts'] = max_attempts - user_attempts
		context['user_max_points'] = attempts.aggregate(Max('points')).values()[0]
		return context

def startquiz(request, pk):
	attempts = Attempt.objects.filter(user=request.user, test__pk=pk)
	attempt_count = attempts.count()
	if not attempts.filter(is_active=True):
		attempt_count = attempt_count + 1
		test = Test.objects.get(pk=pk)
		attempt = Attempt(user=request.user, test=test, number=attempt_count)
		attempt.save()
	return HttpResponseRedirect(reverse('question', kwargs={'pk': pk, 'attempt_count': attempt_count}))

def question(request, pk, attempt_count):
	attempt = Attempt.objects.get(user=request.user, test__pk=pk, number=attempt_count)
	if request.method == "POST":
		q = Attempt.objects.get(
			user=request.user, test__pk=pk, number=attempt_count).current_question()
		form = AnswerForm(request.POST, q_pk=q.id)
		if form.is_valid():
			correct = Answer.objects.filter(question__pk=q.id, 
				is_correct=True).values_list('id', flat=True)
			checked = [answer.pk for answer in form.cleaned_data['answer']]
			if map(int, correct) == map(int, checked):
				attempt.points += Question.objects.get(pk=q.id).points
			try:
				answers = attempt.get_json()
			except ValueError:
				answers = {}
			answers[q.id] = checked
			attempt.set_json(answers)
			attempt.current_q += 1
			attempt.save()
	try:
		q = Attempt.objects.get(
			user=request.user, test__pk=pk, number=attempt_count).current_question()
	except IndexError:
		attempt.close()
		return HttpResponseRedirect(reverse('results', kwargs={'pk': pk, 'attempt_count': attempt_count}))
	form = AnswerForm(q_pk=q.id)
	c = {'question': q, 'form': form, 'attempt_count': attempt_count}
	return render(request, 'quizext/question.html', c)


def results(request, pk, attempt_count):
	attempt = Attempt.objects.get(user=request.user, test__pk=pk, number=attempt_count)
	q = Question.objects.filter(test__pk=pk)
	q_count = q.values('group').distinct().count()
	p_sum = q.aggregate(Sum('points')).values()[0]
	attempt.save()
	user_percent = int(attempt.points) / int(p_sum) * 100
	c = {'test_title': attempt.test.title, 'q_count': q_count, 
		'p_sum': p_sum, 'user_points': attempt.points, 'user_percent': user_percent}
	return render(request, 'quizext/results.html', c)
