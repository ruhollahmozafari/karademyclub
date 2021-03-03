from django.urls import path , reverse, include 
from .models import *
from blog.views import *
from django.views.generic.dates import ArchiveIndexView
from django.views.generic import TemplateView
from . import api_views
app_name='blog'  
from django.core.paginator import Paginator
from rest_framework import routers
router = routers.DefaultRouter()
router.register ('category', CategoryViewAPI)
router.register ('tag', TagViewAPI)

urlpatterns = [
    path('api/',include(router.urls)),

    path('',HomeView.as_view(), name = 'home'),
    path('questions/', QuestionsList.as_view(), name= 'questions'),
    path('questions/<int:pk>/<str:slug>/',QuestionDetail.as_view(), name= 'question-detail'),
    path('questions-in-categories/<str:slug>/',QuestionsInCategories.as_view(), name = 'questions-in-categories'),
    path('questions-in-tag/<str:slug>/',QuestionsInTags.as_view(), name = 'questions-in-tags'),
    path('all-categories/', AllCategories.as_view() , name= 'all-categories'),
    path('all-tags/', AllTags.as_view() , name= 'all-tags'), 
    path('ask/',QuestionCreate.as_view(), name = 'ask'),
    path('update-question/<int:pk>/', update_question,name = 'update-question'),
    path('delete-question/<int:pk>/', QuestionDelete.as_view(), name = 'delete-question'),
    # path('api/categories/',api_views.category_list),
    path('create-like/<str:app>/<str:model>/<int:pk>/', LikeCreate, name = 'create-like'),
    path('answer/<int:pk>/', WriteAnswer.as_view(), name = 'write-answer'),
    path('delete-answer/<int:pk>', DeleteAnswer.as_view(), name = 'delete-answer'),
    path('update-answer/<int:pk>', UpdateAnswer.as_view(), name = 'update-answer'),
    path('all-reports/', ListReport.as_view(), name = 'all-reports'),
    path('create-report/<str:app>/<str:model>/<int:pk>/', CreateReport.as_view(), name = 'create-report'),
    path('delete-report/<int:pk>/', DeleteReport.as_view(), name = 'delete-report'),
    path('question-comment/<int:pk>/', question_comment, name = 'question-comment'),
    path('delete-comment/<int:pk>/', DeleteComment.as_view(), name = 'delete-comment'),
    path('update-comment/<int:pk>/', UpdateComment.as_view(), name = 'update-comment'),
    path('search-question/', SearchResultView.as_view() , name = 'search-results'),
    path('report-detail/<int:pk>/', report_detail , name = 'report-detail'),
    path('report-valid/<int:pk>/' , ReportValid.as_view(), name = 'report-valid' ),
    path('report-invalid/<int:pk>/', ReportInValid.as_view(), name = 'report-invalid'),
    path('contact-us/', ContactUs.as_view(), name = 'contact-us'),
    path('valid-answer/<int:pk>/', MakeValidAnswer, name = 'valid-answer'),


]
 