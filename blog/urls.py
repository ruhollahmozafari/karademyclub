from django.urls import path
from . import views as blog_views
app_name='blog'  

urlpatterns = [
    path('',blog_views.home_page, name = 'home'),
    path('questions/', blog_views.questions, name= 'questions'),#just to show all the questoins
    path('questions/<int:id>/<str:slug>/',blog_views.question_detail, name= 'question-detail'),
    path('questions-in-categories/<str:slug>/',blog_views.questions_in_categories, name = 'questions-in-categories'),
    path('all-categories/', blog_views.all_categories , name= 'all-categories'), # it is not neccesary because it will be shown on the left or right side of the webpage
    path('ask/',blog_views.ask, name = 'ask'),

]     
