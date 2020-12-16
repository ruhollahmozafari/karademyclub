from django.shortcuts import render , redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from clubuser.models import ClubUser
from blog.models import  Category, Question, Answer , Report, Like
from .forms import *
from blog import urls



def user_profile(request, id):
    
    user = ClubUser.objects.get(id = id )
    context = {
        "user":user
    }
    return render(request, 'clubuser/user_profile.html', context)

def user_creation(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST,)
        if signup_form.is_valid():
            new_user = signup_form.save()
            new_user.refresh_from_db()
            new_user.interest = signup_form.cleaned_data.get('interest')
            new_user.save()
            # new_user.set_password(signup_form.cleaned_data["password"])
            new_user.save()
            raw_password = signup_form.cleaned_data.get('password1')
            new_user = authenticate(username=new_user.username, password=raw_password)
            ClubUser.objects.create(user= new_user)
            return redirect("/",) # set this to the profile later

    else:
        signup_form = SignUpForm()

    return render(request, 'clubuser/signup.html', {'signup_form': signup_form})
