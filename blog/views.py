from django.shortcuts import render
from django.http import HttpResponse
from blog.models import ClubUser, Category, Question, Answer , Report, Like

def home_page(request,):
    return render(request , 'blog/home_page.html')
def questions (request,):
    questions = Question.objects.all()
    context = {
        'questions':questions
    }
    return render(request, 'blog/questions.html',context)

def question_detail(request, id ):#showing a question with the detail and the answers
    question= Question.objects.get(id =id )
    answers = Answer.objects.filter(question_id = question.id)
    # {"Question":question,"Answers":answers}
    context = {'question': question}
    # still dont know how to use more than one model in one html render ( got many errors)
    return render(request, 'blog/question_detail.html',context )    

def all_categories(request):
    categories= Category.objects.all()
    context = {
        "Category":categories
    }
    return render(request,'blog/all_categories.html' ,context )


def questions_in_categories(request,title):# all the questions related to specific category(s)
    # still could handle the multiple choices (like selecting from different categories at the same time )
    # questions =[]
    category = Category.objects.get(title = title)
    questions = category.question_set.all()
    context = {
        "Question":questions
    }
    return render(request, 'blog/questions_in_categories.html',context)

def user_profile(request, id):
    
    result = ClubUser.objects.get(id = id )
    return HttpResponse(result)


def ask(request, ):
    return HttpResponse('ask your question here')