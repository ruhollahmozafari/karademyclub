from django.shortcuts import render
from django.http import HttpResponse
from blog.models import  Category, Question, Answer , Report, Like

def home_page(request,):
    return render(request , 'blog/home_page.html')

def questions (request,):
    questions = Question.objects.all()
    context = {
        'questions':questions
    }
    return render(request, 'blog/questions.html',context)

def question_detail(request, id,slug ):#showing a question with the detail and the answers
    question= Question.objects.get(id =id )
    answers = Answer.objects.filter(question_id = question.id)
    context = {
        "question": question,
        "answers":answers
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

def ask(request, ):
    return render(request, 'blog/ask.html',)