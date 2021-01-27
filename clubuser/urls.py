from django.urls import path
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from .views import *
from django.views.generic import TemplateView

# from blog.views import views as question_views
app_name='clubuser'  

urlpatterns = [
    path('profile/<int:pk>/',profile, name = 'profile'),
    path('signup/',UserCreation.as_view(), name= 'signup'),
    path('login/', login, name= 'login'),
    path('logout/',logout , name = 'logout'),
    path('update-profile/<int:pk>/', edit_profile, name = 'update-profile'),
    path('profile/change-pass/', PassChangeView.as_view(), name= 'change-pass'),
    path('profile/pass-changed/',TemplateView.as_view(template_name = 'clubuser/pass-changed.html'), name = 'pass-changed' ),
    path('my-questions/<int:pk>/', MyQuestion.as_view(), name= 'my-questions'),
    path('my-notifications/<int:pk>', NotificationView.as_view(), name ='my-notifs'),
    

]


