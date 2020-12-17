from django import forms
from .models import Question


class Ask(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'body', 'category','tag')




            