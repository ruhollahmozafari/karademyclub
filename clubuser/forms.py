from django import forms
from .models import ClubUser
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ClubUser
from blog.models import Category, Report
from blog.forms import *


class SignUpForm(UserCreationForm):# try it by inheriting from UserCreationForm and see what will happen use this link : https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
    interest = forms.ModelChoiceField(queryset= Category.objects.all())
    image = forms.ImageField( required= False)
    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email','password1', 'password2','interest',"image"]
        # widgets = {
        #     'username' : forms.TextInput(attrs={
        #         'cols': 6, 'rows':2,
        #         'class': 'form-control',
        #         'placeholder': 'username like roohollah123 '
        #     }),
        #     'first_name' : forms.TextInput(attrs={
        #         'cols': 6, 'rows':2,
        #         'class': 'form-control',
        #         'placeholder': 'rewrite your tags here '
        #     }),
        #     'last_name' : forms.TextInput(attrs={
        #         'cols': 6, 'rows':2,
        #         'class': 'form-control',
        #         'placeholder': 'rewrite your tags here '
        #     }),
        #     'email' : forms.TextInput(attrs={
        #         'cols': 6, 'rows':2,
        #         'class': 'form-control',
        #         'placeholder': 'rewrite your tags here '
        #     }),
        #     'password1' : forms.TextInput(attrs={
        #         'cols': 6, 'rows':2,
        #         'class': 'form-control',
        #         'placeholder': 'rewrite your tags here '
        #     }),
        #     'password2' : forms.TextInput(attrs={
        #         'cols': 10, 'rows': 10,
        #         'class': 'form-control',
        #         'placeholder': 'rewrite your tags here '
        #     }),       
        # }



class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name","last_name","email",)


class ClubUserUpdateForm(forms.ModelForm):
    class Meta:
        model = ClubUser
        fields = [
            "interest","profile_image",
            ]