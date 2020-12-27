from django.urls import path
from . import views as clubuser_views
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from .views import UserCreation,UserUpdate


# from blog.views import views as question_views
app_name='clubuser'  

urlpatterns = [
    path('profile/<int:id>/',clubuser_views.profile, name = 'profile'),
    path('signup/',UserCreation.as_view(), name= 'signup'),
    path('login/', clubuser_views.login, name= 'login'),
    path('logout/', clubuser_views.logout , name = 'logout'),
    path('update-profile/<int:pk>/', UserUpdate.as_view(), name = 'update-profile'),
    # path('login/', LoginView.as_view(), {'template_name': 'login.html'}, name='login'),
#   path('login/',clubuser_views.login, name = 'login'),
]


