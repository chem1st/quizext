# encoding: UTF-8
from django.db.models import Sum
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Test, Question, Answer, Attempt
from .forms import QuestionForm


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
		context['q_num'] = q.values('group').distinct().count()
		context['sum'] = q.aggregate(Sum('points')).values()[0]
		context['time'] = Test.objects.filter(pk=self.kwargs['pk']).values_list('time', 
			flat=True)[0]/3600
		context['user_attempts'] = Attempt.objects.filter(user=self.request.user, test__pk=self.kwargs['pk']).count()
		return context


def question(request, pk, q_set):
	q = Question.objects.filter(test__pk=pk).filter(group=q_set).order_by('?').first()
	next_q = Question.objects.filter(group__gt=q_set).order_by('group').first()
	c = {'question': q, 'next': next_q}
	if request.method == "POST":
		if int(q_set) == 1:
			attempt_count = Attempt.objects.filter(user=request.user, test__pk=pk).count() + 1
			test = Test.objects.get(pk=pk)
			attempt = Attempt(user=request.user, test=test, number=attempt_count)
			attempt.save()
		else:
			ca = Answer.objects.filter(question__pk=request.POST.get('q_pk'), 
				is_correct=True).values_list('id', flat=True)
			ra = request.POST.getlist('answer')
			if map(int, ca) == map(int, ra):
				response = True
			c['response'] = response
	return render(request, 'quizext/question.html', c)


def results(request, pk):
	c = {}
	return render(request, 'quizext/results.html', c)