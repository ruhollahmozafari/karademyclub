from django.urls import path
from . import views as clubuser_views
app_name='clubuser'  

urlpatterns = [
    path('user-profile/<int:id>/',clubuser_views.user_profile, name = 'user-profile'),


]     
