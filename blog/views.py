from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse , HttpResponseRedirect
from blog.models import  Answer, Tag , Category, Question
from django.contrib import messages 
from django.contrib.auth import decorators
from .forms import Ask
from clubuser.forms import *

def home_page(request,):
    return render(request , 'blog/home_page.html')

def questions (request,):
    questions = list(Question.objects.all())
    context = {
        'questions':questions
    }
    return render(request, 'blog/questions.html',context)

def question_detail(request, id,slug ):#showing a question with the detail and the answers
    question= get_object_or_404(Question, id = id)
    answers = Answer.objects.filter(question_id = question.id)
    tags = list(question.tag.all())
    context = {
        "question": question,
        "answers":answers,
        "tags":tags,
    }
    return render(request, 'blog/question_detail.html',context )    

def all_categories(request):
    categories= Category.objects.all()
    context = {
        "categories":categories
    }
    return render(request,'blog/all_categories.html' ,context )

def questions_in_categories(request,slug):
    category = Category.objects.get(slug = slug)
    questions = category.question_set.all()

    context = {
        "questions":questions
    }
    return render(request, 'blog/questions_in_categories.html',context)

def ask(request):
    if request.user.is_anonymous:
        
        return render(request,'blog/enter_to_ask.html',)
    else:
        return ask_verified(request)

@login_required()
def ask_verified(request, ):
    form = Ask()
    if request.method == 'POST':
        form = Ask(request.POST)
        if form.is_valid():
            question = form.save()
            question.user = request.user
            question.save()
            form= Ask()
            messages.success(request, "Question succesfully created, wait for your answer ")
    else:
        form = Ask()
    return render(request, 'blog/ask.html',{'form': form})

def enter_to_ask(request):
    return render(request, 'blog/enter_to_ask.html',)


