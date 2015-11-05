from django import forms
from .models import Answer


class IntegerAnswerForm(forms.Form):
	answer = forms.CharField(max_length=16)


class MultipleChoiceAnswerForm(forms.Form):
    answer = forms.ModelMultipleChoiceField(
        queryset = Answer.objects.all(),
        widget = forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        q_pk = kwargs.pop('q_pk', None)
        super(MultipleChoiceAnswerForm, self).__init__(*args, **kwargs)
        self.fields['answer'].queryset = Answer.objects.filter(question__pk=q_pk)
