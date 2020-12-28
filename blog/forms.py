from django import forms
from .models import Question

class Ask(forms.ModelForm):
    tag_char = forms.CharField(max_length= 100,  required = False)
    class Meta:
        model = Question
        fields = ('title', 'body', 'category')

    # def making_tags(self,):
    #     tag_list =self.tag_char.split()
    #     return tag_list



            