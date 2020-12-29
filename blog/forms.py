from django import forms
from .models import Question, Answer,Report

class Ask(forms.ModelForm):
    tag_char = forms.CharField(max_length= 100,  required = False)
    class Meta:
        model = Question
        fields = ('title', 'body', 'category')

class UpdateQuestion(forms.ModelForm):
    tag_char = forms.CharField(max_length= 100,  required = False)

    class Meta :
        model =Question
        fields = ('title', 'body', 'category',)
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ("body",)

class ReportForm(forms.ModelForm):
    
    class Meta:
        model = Report
        fields = [
            
            'reason',
            'detail',
        ]


