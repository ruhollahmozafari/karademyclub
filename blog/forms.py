from django import forms
from djrichtextfield.widgets import RichTextWidget
from .models import Question


class Ask(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('title', 'body', 'interest',)
        