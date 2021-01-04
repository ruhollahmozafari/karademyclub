from django.shortcuts import render , redirect
from django.contrib.auth import authenticate 
from django.urls import reverse ,reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import auth
from django.contrib.auth.forms import  AuthenticationForm, PasswordChangeForm
from django.contrib.auth.views import  PasswordChangeView
from django.http import HttpResponse
from clubuser.models import ClubUser
from django.contrib.messages.views import SuccessMessageMixin
from blog.models import  Category, Question, Answer , Report,Tag
from django.views.generic import ListView,DetailView,UpdateView, DeleteView, CreateView
from .forms import *
from blog import urls
from blog.views import *
from django.contrib.auth import login as auth_login
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class PassChangeView(SuccessMessageMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = 'registration/change-pass.html'
    # success_url = ('blog:question')
    success_message = ( f'your pass have chnaged dear user !')
    success_url= '/questions'


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

class UserCreation(CreateView):
    def post(self, request,*args, **kwargs):
        signup_form = SignUpForm(request.POST,request.FILES)
        if signup_form.is_valid():
            new_user = signup_form.save()
            new_user.refresh_from_db()
            interest1 = signup_form.cleaned_data.get('interest')
            new_user = authenticate(username=signup_form.cleaned_data.get('username'), password=signup_form.cleaned_data.get('password1'))
            new_user.save()
            new1 = ClubUser.objects.create(user = new_user)
            new1.interest.add(interest1)
            new1.profile_image = signup_form.cleaned_data.get('image')# adding picture failed, any suggestion ?
            new1.save()
            subject = f'Welcome to karademy dear {new_user.first_name},'
            message = f'You can improve your skill and knowledge in this community, It is a honnor to have you here.' 
            recepient = str(new_user.email)
            send_mail(subject, message, 'ruhytest@gmail.com', [recepient], fail_silently = True)
            auth_login(request, new_user)
        return redirect('blog:questions') 
        
    def get(self, request,*args, **kwargs):
        signup_form = SignUpForm()
        return render(request, 'clubuser/signup.html', {'signup_form': signup_form})

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

    context = {'u_form': u_form,'c_form': c_form}
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

