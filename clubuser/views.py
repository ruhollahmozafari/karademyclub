from django.shortcuts import render , redirect
from django.contrib.auth import authenticate 
from django.urls import reverse ,reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import auth
from django.contrib.auth.forms import  AuthenticationForm, PasswordChangeForm
from django.contrib.auth.views import  PasswordChangeView
from django.http import HttpResponse
from clubuser.models import ClubUser
from blog.models import  Category, Question, Answer , Report,Tag
from django.views.generic import ListView,DetailView,UpdateView, DeleteView, CreateView
from .forms import *
from blog import urls
from blog.views import *
from django.contrib.auth import login as auth_login

class PassChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'registration/change-pass.html'
    # success_url = ('blog:question')
    success_url= 'blog/questions'


def profile(request, pk):
    # you can use this method by having 'user.clubuser.pk' in the tample base.html... 
    # or you can chage the user.clubuser.pk to user.pk and uncooment the two following lines here
    user1 = User.objects.get(id = pk)
    main_pk = user1.clubuser.id
    profile = get_object_or_404(ClubUser, pk = main_pk )
    
    context = {
        "profile":profile
    }
    return render(request, 'clubuser/user_profile.html', context)
    # u_form = UserUpdateForm(instance = request.user)
    # c_form = ClubUserUpdateForm(instance= request.user.clubuser)
    # context["u_form"] = "u_form"
    # context["c_form"] = "c_form"
    
    # return render(request, 'clubuser/user_profile.html', context)

class UserCreation(CreateView):
    def post(self, request,*args, **kwargs):
        signup_form = SignUpForm(request.POST,request.FILES)
        if signup_form.is_valid():
            new_user = signup_form.save()
            new_user.refresh_from_db()
            # new_user.interest = signup_form.cleaned_data.get('interest')
            # new_user.profile_image  = signup_form.cleaned_data.get('image')
            # new_user.set_password(signup_form.cleaned_data["password"])
            # new_user.club_user.profile_image = signup_form.cleaned_data.get('image')
            interest1 = signup_form.cleaned_data.get('interest')
            # new_user.save()
            new_user = authenticate(username=signup_form.cleaned_data.get('username'), password=signup_form.cleaned_data.get('password1'))
            new_user.save()
            new1 = ClubUser.objects.create(user = new_user)
            new1.interest.add(interest1)
            new1.profile_image = signup_form.cleaned_data.get('image')# adding picture failed, any suggestion ?
            new1.save()
            # if user is not None: add these later to go to another page
            auth_login(request, new_user)
        return redirect('blog:questions') 
        
    def get(self, request,*args, **kwargs):
        signup_form = SignUpForm()
        return render(request, 'clubuser/signup.html', {'signup_form': signup_form})

class UserUpdate(UpdateView):
    template_name = 'clubuser/update-profile.html'
    model = User
    fields = [
        'first_name','last_name', 'email'
    ]
    success_url = reverse_lazy('blog:questions')
    
    # this class will finish later
    # fields = '__all__'
    # def get_object(self, *args, **kwargs):
    #     user = get_object_or_404(User, pk=self.kwargs['pk'])
    #     user.first_name = self.kwargs['first_name']
    #     user.last_name = self.kwargs['last_name']
    #     user.email = self.kwargs['email']

    #     return user.clubuser

    # def get_success_url(self, *args, **kwargs):
    #     return reverse_lazy('blog:home')
@login_required
def edit_profile(request,*args, **kwargs):
    temp = ClubUser.objects.get(id = kwargs['pk'])
    user_id = temp.user.id

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        c_form = ClubUserUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.clubuser)
        if u_form.is_valid() and c_form.is_valid():
            u_form.save()
            c_form.save()
            messages.success(request, f'Your account has been updated!')

            return HttpResponseRedirect (reverse_lazy('clubuser:profile', args= [user_id]) )

    else:
        u_form = UserUpdateForm(instance=request.user)
        c_form = ClubUserUpdateForm(instance=request.user.clubuser)

    context = {
        'u_form': u_form,
        'c_form': c_form
    }

    return render(request, 'clubuser/update-profile.html', context)


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

