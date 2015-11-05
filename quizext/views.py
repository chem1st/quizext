# encoding: UTF-8
from __future__ import division
from django.core.urlresolvers import reverse
from django.db.models import Max, Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Test, Question, Answer, Attempt
from .forms import IntegerAnswerForm, MultipleChoiceAnswerForm


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
		context['attempts_loop'] = range(0, user_attempts)
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
	if attempt.endtime:
		return HttpResponseRedirect(reverse('results', 
			kwargs={'pk': pk, 'attempt_count': attempt_count }))
	if request.method == "POST":
		q = attempt.current_question()
		if q.is_free:
			form = IntegerAnswerForm(request.POST)
		else:
			form = MultipleChoiceAnswerForm(request.POST, q_pk=q.id)
		if form.is_valid():
			attempt.add_answered_question(form.cleaned_data['answer'])
		else:
			if request.POST.get("skip"):
				attempt.add_skipped_question()
			else:
				c = {'question': q, 'form': form, 'attempt_count': attempt_count, 
					'timetill': attempt.timetill }
				return render(request, 'quizext/question.html', c)
		attempt.next_question()
	try:
		q = attempt.current_question()
	except IndexError:
		q = attempt.next_lap()
		if not q:
			attempt.close()
			return HttpResponseRedirect(reverse('results', 
				kwargs={'pk': pk, 'attempt_count': attempt_count }))
	if q.is_free:
		form = IntegerAnswerForm()
	else:
		form = MultipleChoiceAnswerForm(q_pk=q.id)
	c = {'question': q, 'form': form, 'attempt_count': attempt_count, 'timetill': attempt.timetill }
	return render(request, 'quizext/question.html', c)


def close(request, pk, attempt_count):
	if request.method == "POST":
		attempt = Attempt.objects.get(user=request.user, test__pk=pk, number=attempt_count)
		if attempt.is_active:
			attempt.close()
	return HttpResponse(status=200)


def results(request, pk, attempt_count):
	attempt = Attempt.objects.get(user=request.user, test__pk=pk, number=attempt_count)
	test = Test.objects.get(pk=pk)
	q_count = test.count_questions()
	answered = attempt.count_answered()
	p_sum = test.max_points()
	rating = round(attempt.points / p_sum * 100, 2)
	c = {'attempt': attempt, 'test': test, 'q_count': q_count, 'answered': answered, 
		'p_sum': p_sum, 'rating': rating}
	return render(request, 'quizext/results.html', c)
