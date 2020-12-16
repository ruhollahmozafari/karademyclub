from django.urls import path
from . import views as clubuser_views
# from blog.views import views as question_views
app_name='clubuser'  

urlpatterns = [
    path('profile/<int:id>/',clubuser_views.user_profile, name = 'profile'),
    path('signup/',clubuser_views.user_creation, name= 'signup'),
    # path('signup/',question_views.)
]     
