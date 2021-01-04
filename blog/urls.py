from django.urls import path
from django.urls import reverse
from .models import *
from blog.views import *
from django.views.generic.dates import ArchiveIndexView
from django.views.generic import TemplateView
from . import api_views
app_name='blog'  

urlpatterns = [
    path('',TemplateView.as_view(template_name = 'blog/home_page.html'), name = 'home'),
    path('questions/', ArchiveIndexView.as_view(model=Question,template_name = 'blog/questions.html', date_field="created_date"), name= 'questions'),#just to show all the questoins
    path('questions/<int:pk>/<str:slug>/',QuestionDetail.as_view(), name= 'question-detail'),
    path('questions-in-categories/<str:slug>/',QuestionsInCategories.as_view(), name = 'questions-in-categories'),
    path('questions-in-tag/<str:slug>/',QuestionsInTags.as_view(), name = 'questions-in-tags'),
    path('all-categories/', AllCategories.as_view() , name= 'all-categories'), # it is not neccesary because it will be shown on the left or right side of the webpage
    path('all-tags/', AllTags.as_view() , name= 'all-tags'), 
    path('ask/',QuestionCreate.as_view(), name = 'ask'),
    path('update-question/<int:pk>/', QuestionUpdate.as_view(),name = 'update-question'),
    path('delete-question/<int:pk>/', QuestionDelete.as_view(), name = 'delete-question'),
    path('api/categories/',api_views.category_list),
    path('create-like/<str:app>/<str:model>/<int:pk>/', LikeCreate, name = 'create-like'),
    # path('like-answer/<int:pk>/', LikeAnswerView, name = 'like-answer'),
    path('answer/<int:pk>/', WriteAnswer.as_view(), name = 'write-answer'),
    path('delete-answer/<int:pk>', DeleteAnswer.as_view(), name = 'delete-answer'),
    path('update-answer/<int:pk>', UpdateAnswer.as_view(), name = 'update-answer'),
    path('all-reports/', ListReport.as_view(), name = 'all-reports'),
    path('create-report/<str:app>/<str:model>/<int:pk>/', CreateReport.as_view(), name = 'create-report'),
    path('question-comment/<int:pk>/', question_comment, name = 'question-comment'),
    path('delete-comment/<int:pk>/', DeleteComment.as_view(), name = 'delete-comment'),
    path('update-comment/<int:pk>/', UpdateComment.as_view(), name = 'update-comment'),
    path('search-question/', QuestionResultsView.as_view() , name = 'search-results'),

]
 