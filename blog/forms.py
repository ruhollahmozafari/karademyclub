from django import forms
from .models import Question

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
