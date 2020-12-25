from django.urls import path
from django.urls import reverse
from .models import *
from . import views as blog_views
from blog.views import QuestionDetail, AllCategories,QuestionsInCategories,QuestionUpdate,QuestionDelete, QuestionCreate
from django.views.generic.dates import ArchiveIndexView
from django.views.generic import TemplateView
from . import api_views
app_name='blog'  

urlpatterns = [
    path('',TemplateView.as_view(template_name = 'blog/home_page.html'), name = 'home'),
    path('questions/', ArchiveIndexView.as_view(model=Question,template_name = 'blog/questions.html', date_field="created_date"), name= 'questions'),#just to show all the questoins
    path('questions/<int:id>/<str:slug>/',QuestionDetail.as_view(), name= 'question-detail'),
    path('questions-in-categories/<str:slug>/',QuestionsInCategories.as_view(), name = 'questions-in-categories'),
    path('all-categories/', AllCategories.as_view() , name= 'all-categories'), # it is not neccesary because it will be shown on the left or right side of the webpage
    path('ask/',QuestionCreate.as_view(), name = 'ask'),
    path('update-question/<int:pk>/', QuestionUpdate.as_view(),name = 'update-question'),
    path('delete-question/<int:pk>/', QuestionDelete.as_view(), name = 'delete-question'),
    path('api/categories/',api_views.category_list),

]
