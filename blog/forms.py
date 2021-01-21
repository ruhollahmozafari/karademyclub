from django import forms
from .models import *
from clubuser.models import ClubUser
from django.contrib.auth.models import User

class Ask(forms.ModelForm):
    tag_char = forms.CharField(max_length= 100,  required = False, widget=forms.Textarea(attrs={'cols': 30, 'rows': 3}))

    class Meta:
        model = Question
        fields = ('title', 'body', 'category',)
        widgets = {
            'title' : forms.TextInput(attrs={
                'cols': 10, 'rows': 10,
                'class': 'form-control',
                'placeholder': 'rewrite your tags here '
            }),
        }

class UpdateQuestionForm(forms.ModelForm):
    tag_char = forms.CharField(max_length= 100,  required = False)

    class Meta :
        model =Question

        fields = ('title', 'body', 'category', 'tag_char')

        widgets = {
            'tag_char' : forms.TextInput(attrs={
                'cols': 20, 'rows': 30,
                'class': 'form-control',
                'placeholder': 'rewrite your tags here '
            }),
        }

class AnswerForm(forms.ModelForm):
    
    class Meta:
        model = Answer
        fields = ("body",)
        
class ReportForm(forms.ModelForm):
    
    class Meta:
        model = Report
        fields = ['reason','detail',]
        widgets = {
            'detail' : forms.TextInput(attrs={
                'cols': 20, 'rows': 30,
                'class': 'form-control',
                'placeholder': 'give us more detail for report reason '
            }),
        }

class QuestionCommentForm(forms.ModelForm):

    class Meta:
        model = QuestionComment
        fields = ("body",)
        widgets = {
            'body' : forms.TextInput(attrs={
                'cols': 20, 'rows': 30,
                'class': 'form-control',
                'placeholder': 'write your comment for this answer here'
            }),
        }

class UpdateCommentFrom(forms.ModelForm):
    
    class Meta:
        model = QuestionComment
        fields = ("body",)
        widgets = {
            'body' : forms.TextInput(attrs={
                'cols': 20, 'rows': 30,
                'class': 'form-control',
                'placeholder': 'write your comment for this answer here'
            }),
        }



