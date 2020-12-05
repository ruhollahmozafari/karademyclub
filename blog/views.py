from django.shortcuts import render
from django.http import HttpResponse
from blog.models import ClubUser, Category, Question, Answer , Report, Like

def home_page(request,):
    return HttpResponse('welcome to karademy club \n this is homepage')

def quesions (request,):
    questions = Question.objects.all()
    context = {
        'quesions':questions
    }
    return HttpResponse(context)

def home_page(request , id = 1):
    q = Question.objects.get(id= id)
    result = f'title : {q.title} , slug : {q.slug} , id {q.id} author : {q.user_id} ,body : {q.body} , updated_date ; {q.updated_date} ,category : {q.category}'
    return HttpResponse(result)


git
    