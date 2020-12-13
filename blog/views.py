from django.shortcuts import render , get_object_or_404
from django.http import HttpResponse , HttpResponseRedirect
from blog.models import  *
from .forms import Ask

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
    cats = list(question.interest.all())
    context = {
        "question": question,
        "answers":answers,
        "cats":cats,
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
    if request.method == 'POST':
        question_form = Ask(request.POST)
        if question_form.is_valid():
            question_form.save()
            return HttpResponseRedirect('blog:questions')
    else:
        question_form = Ask()
        context = {'question_form': question_form}
    return render(request, 'blog/ask.html',context)