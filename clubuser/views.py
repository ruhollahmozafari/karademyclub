from django.shortcuts import render , redirect
from django.contrib.auth import authenticate 
from django.shortcuts import get_object_or_404
from django.contrib import auth
from django.contrib.auth.forms import  AuthenticationForm
from django.http import HttpResponse
from clubuser.models import ClubUser
from blog.models import  Category, Question, Answer , Report, Like
from django.views.generic import ListView,DetailView,UpdateView, DeleteView, CreateView
from .forms import *
from blog import urls


def profile(request, id):
    # you can use this method by having 'user.clubuser.id' in the tample base.html or you can chage the user.clubuser.id to user.id and uncooment the two following lines here
    user1 = User.objects.get(id = id)
    main_id = user1.clubuser.id
    profile = get_object_or_404(ClubUser, pk = main_id )
    # profile = request.user.get_profile()
    # user = profile
    context = {
        "profile":profile
    }
    return render(request, 'clubuser/user_profile.html', context)

class UserCreation(CreateView):
    def post(self, request):
        signup_form = SignUpForm(request.POST,)
        if signup_form.is_valid():
            new_user = signup_form.save()
            new_user.refresh_from_db()
            # new_user.interest = signup_form.cleaned_data.get('interest')
            # new_user.profile_image  = signup_form.cleaned_data.get('image')
            # new_user.set_password(signup_form.cleaned_data["password"])
            # new_user.club_user.profile_image = signup_form.cleaned_data.get('image')
            interest1 = signup_form.cleaned_data.get('interest')
            new_user.save()
            raw_password = signup_form.cleaned_data.get('password1')
            new_user = authenticate(username=new_user.username, password=raw_password)
            new1 = ClubUser.objects.create(user = new_user,)
            new1.interest.add(interest1)
            # new_user.user_clubuser.profile_image = signup_form.cleaned_data.get('image')# adding picture failed, any suggestion ?
            new1.save()
        return redirect('clubuser:login') 

    def get(self, request):
        signup_form = SignUpForm()
        return render(request, 'clubuser/signup.html', {'signup_form': signup_form})


def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password = request.POST['password'])
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            return render (request,'registration/login.html/', {'error':'Username or password is incorrect!'})
    else:
        return render(request,'registration/login.html/')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
    return render(request, 'registration/logout.html')
