from django import forms
from .models import ClubUser
from django.contrib.auth.models import User



class SignUpForm(forms.ModelForm):# try it by inheriting from UserCreationForm and see what will happen use this link : https://simpleisbetterthancomplex.com/tutorial/2017/02/18/how-to-create-user-sign-up-view.html


    class Meta:
        model =   ClubUser
        fields = ['fname', 'lname', 'email','gender', ] 

        