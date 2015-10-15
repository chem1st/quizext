from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView
from .models import Test, Question
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
		context['q_num'] = Question.objects.filter(test__pk=self.kwargs['pk']).values('group').distinct().count()
		return context


class QuestionFormView(FormView):
	form_class = QuestionForm
	template_name = 'quizext/question.html'
	success_url = reverse_lazy('question')

	def form_valid(self, form):
		return super(QuestionFormView, self).form_valid(form)
