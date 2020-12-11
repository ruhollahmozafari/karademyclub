from django.shortcuts import render
from django.http import HttpResponse
from clubuser.models import ClubUser
from blog.models import  Category, Question, Answer , Report, Like



def user_profile(request, id):
    
    user = ClubUser.objects.get(id = id )
    context = {
        "user":user
    }

    return render(request, 'clubuser/user_profile.html', context)

