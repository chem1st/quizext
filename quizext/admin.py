from django.contrib import admin
from .models import Test, Question, Answer


class HideModel(admin.ModelAdmin):
	def get_model_perms(self, request):
		return {}

class AnswerInline(admin.StackedInline):
	model = Answer

class QuestionAdmin(admin.ModelAdmin):
	list_display = ['__unicode__', 'test', 'group']
	inlines = [
		AnswerInline,
	]

class QuestionInline(admin.StackedInline):
	model = Question

class TestAdmin(admin.ModelAdmin):
	inlines = [
		QuestionInline,
	]

admin.site.register(Test, TestAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, HideModel)
