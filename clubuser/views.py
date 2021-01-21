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
from blog.models import  *
from django.views.generic import ListView,DetailView,UpdateView, DeleteView, CreateView
from .forms import *
from blog import urls
from blog.views import *
from django.contrib.auth import login as auth_login
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "layouts/password/password_reset_email.html"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'ruhytest@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
                    
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="layouts/password/password_reset.html", context={"password_reset_form":password_reset_form})


@method_decorator(login_required, name = 'dispatch')
class PassChangeView(SuccessMessageMixin, PasswordChangeView):

    form_class = PasswordChangeForm
    template_name = 'registration/change-pass.html'
    success_message = ( f'your pass have changed dear user !')
    success_url= '/questions'


def profile(request, pk):
    # you can use this method by having 'user.clubuser.pk' in the tample base.html... 
    # or you can chage the user.clubuser.pk to user.pk and uncooment the two following lines here
    user1 = User.objects.get(id = pk)
    main_pk = user1.clubuser.id
    profile = get_object_or_404(ClubUser, pk = main_pk )
    questions = Question.objects.filter(user = user1)

    context = {
        "profile":profile,
        "questions":questions,
    }
    return render(request, 'clubuser/user_profile.html', context)


class MyQuestion(ListView):
    model = Question
    template_name = 'clubuser/question_archive.html'
    context_object_name = 'questions'
    def get_queryset(self,*args, **kwargs):
        return Question.objects.filter(user__id =  self.kwargs['pk'])
    

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
            new1.profile_image = signup_form.cleaned_data.get('image')
            new1.save()
            #sending email to the new user to say welcome
            subject = f'Welcome to karademy dear {new_user.first_name},'
            message = f'You can improve your skill and knowledge in this community, It is a honnor to have you here.' 
            recepient = str(new_user.email)
            send_mail(subject, message, 'ruhytest@gmail.com', [recepient], fail_silently = True)
            auth_login(request, new_user)
            messages.success(request, "Your account has been created, welcome ")
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


class NotificationView(ListView):
    template_name = 'clubuser/my_notifs.html'
    context_object_name = 'notifs'
    def get_queryset(self):
        notifs =Notification.objects.filter(user__pk = self.kwargs['pk']).order_by('-created_date')

        #to make a new notif into read one
        for notif in notifs:
            if notif.view < 2 :
                notif.view += 1
            notif.save()
        return notifs





