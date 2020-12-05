from django.urls import path
from . import views as blog_views
app_name='blog'  

urlpatterns = [
    path('',blog_views.home_page, name = 'home'),
    path('quesions/', blog_views.quesions),#just to show all the questoins
    path('quesoins/<id>',blog_views.question_detail)
    path('categories/', blog_views.categories)
    path('categories/<str:slug>',blog_views.question_category)
    path('profile/<str:slug>/<id:id>'/blog_views.user_profile)

]     