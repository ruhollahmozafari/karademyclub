from django.shortcuts import render , redirect
from django.http import HttpResponse
from clubuser.models import ClubUser
from blog.models import  Category, Question, Answer , Report, Like
from .forms import *
# from blog import urls



def user_profile(request, id):
    
    user = ClubUser.objects.get(id = id )
    context = {
        "user":user
    }
    return render(request, 'clubuser/user_profile.html', context)

def user_creation(request):
    if request.method == 'POST':
        signup_form = SignUpForm(request.POST,)
        if signup_form.is_valid:
            signup_form.save()
            return redirect("/questions/") # set this to the profile later
    else:
        signup_form = SignUpForm()
    return render(request, 'clubuser/signup.html', {'signup_form': signup_form})
