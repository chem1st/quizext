from django import forms
from .models import Answer


class AnswerForm(forms.Form):
    answer = forms.ModelMultipleChoiceField(
        queryset = Answer.objects.all(),
        widget = forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        q_pk = kwargs.pop('q_pk', None)
        super(AnswerForm, self).__init__(*args, **kwargs)
        self.fields['answer'].queryset = Answer.objects.filter(question__pk=q_pk)
