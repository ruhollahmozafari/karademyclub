from django import forms
from .models import ClubUser
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ClubUser



class SignUpForm(UserCreationForm):# try it by inheriting from UserCreationForm and see what will happen use this link : https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html
    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email','password1', 'password2',]

    