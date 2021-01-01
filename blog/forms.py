from django import forms
from .models import *
from clubuser.models import ClubUser
from django.contrib.auth.models import User

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
        fields = ['reason','detail',]


class QuestionCommentForm(forms.ModelForm):
    # body = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Add a comment...'}))
    class Meta:
        model = QuestionComment
        fields = ("body",)

