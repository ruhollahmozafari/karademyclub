from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse ,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse , HttpResponseRedirect
from blog.models import  Answer, Tag , Category, Question
from django.contrib import messages 
from django.utils.decorators import method_decorator
from django.contrib.auth import decorators
from .forms import Ask
from clubuser.forms import *
from django.views import View
from django.views.generic import ListView,DetailView,UpdateView, DeleteView, CreateView
from hitcount.views import HitCountDetailView



class QuestionDetail(HitCountDetailView):# we can use method 1 or 2
    #method 1
    template_name = 'blog/question_detail.html'
    model = Question
    context_object_name = 'question'
    count_hit = True
    
#this is not a good approach to do it so the hitcounter was used
    # def get_object(self):# getting the question to show while adding one to the views 
    #     object = super(QuestionDetail, self).get_object()
    #     object.views +=1
    #     object.save()
    #     return object
    
    def get_context_data(self, **kwargs):# fetching the answers of the same question
        context = super(QuestionDetail,self).get_context_data(**kwargs)
        context["answers"]= Answer.objects.filter(question_id= self.kwargs['pk'])
        return context
    
    


class AllCategories(ListView):
    model = Category
    template_name = 'blog/all_categories.html'
    context_object_name = 'categories'


class QuestionsInCategories(ListView,): 
    model = Question
    template_name = 'blog/questions_in_categories.html'
    context_object_name = 'questions'
    
    def get_queryset(self):
        self.category =get_object_or_404(Category, slug = self.kwargs['slug'])
        return Question.objects.filter(category = self.category)
    
    def get_context_data(self, **kwargs):
        context = super(QuestionsInCategories,self).get_context_data(**kwargs)
        context["category"] =self.category 
        return context


@method_decorator(login_required, name = 'dispatch')
class QuestionCreate(CreateView):
    def get(self, request ):
        form = Ask()
        form = Ask()
        return render(request, 'blog/ask.html',{'form': form})

    def post(self, request):
        form = Ask(request.POST)
        if form.is_valid():
            question = form.save()
            question.user = request.user
            question.save()
            form= Ask()
            messages.success(request, "Question succesfully created, wait for your answer ")
        return HttpResponseRedirect(reverse_lazy('blog:questions'))
    
@method_decorator(login_required, name = 'dispatch')
class QuestionUpdate(UpdateView):#need to check the user log in and writer match
        model = Question
        fields = ['title', 'body', 'category']
        template_name = 'blog/update_question.html'
        success_url= reverse_lazy('blog:questions')


@method_decorator(login_required, name = 'dispatch')
class QuestionDelete(DeleteView):

    def post(self,request):
        
        if request.user == question.user:
            template_name = 'blog/delete-question.html'
            success_url = reverse_lazy('blog:questions')
    



# from this line on are the the funciotns which was created at first then the whole view was turned to CBV
# kept it for the sake of learning


# def ask(request):# this is gonna be a pop up rather than a single page
#     if request.user.is_anonymous:
        
#         return render(request,'blog/enter_to_ask.html',)
#     else:
#         return ask_verified(request)


# @login_required()
# def ask_verified(request, ):
#     form = Ask()
#     if request.method == 'POST':
#         form = Ask(request.POST)
#         if form.is_valid():
#             question = form.save()
#             question.user = request.user
#             question.save()
#             form= Ask()
#             messages.success(request, "Question succesfully created, wait for your answer ")
#     else:
#         form = Ask()
#     return render(request, 'blog/ask.html',{'form': form})


# #///////////////////home///////////////
# class Home(View):
#     template_name = 'blog/home_page.html'
#     def get(self, request,*args, **kwargs):
#         return render(request, self.template_name)  


# def home_page(request,):
#     return render(request , 'blog/home_page.html')
#//////////////////home/////////////////////////////

#/////////////////QuestionList//////////////////////////////////
# class QuestionsList(ListView):
#     template_name = 'blog/questions.html'
#     model = Question

    # paginate_by = 2 >>> this must be completetd later inorder to prevent long pages (super necessary)
    #  
    # context_object_name = 'questoins' >>> not necessary cuase we only have one model and one context 


# def questions (request,):
#     questions = list(Question.objects.all())
#     context = {
#         'questions':questions
#     }
#     return render(request,'blog/questions.html',context)
#/////////////////QuestionList//////////////////////////////////

#///////////////////QuestionDetial/////////////////////////////


# def all_categories(request):
#     categories= Category.objects.all()
#     context = {
#         "categories":categories
#     }
#     return render(request,'blog/all_categories.html' ,context )
#///////////////////AllCategories////////////////////////

#/////////////QuestionsInCategories//////////////////////

# def questions_in_categories(request,slug):
#     category = Category.objects.get(slug = slug)
#     questions = category.question_set.all()

#     context = {
#         "questions":questions
#     }
#     return render(request, 'blog/questions_in_categories.html',context)

#/////////////QuestionsInCategories//////////////////////
# def question_detail(request, id,slug ):#showing a question with the detail and the answers
#     question= get_object_or_404(Question, id = id)
#     answers = Answer.objects.filter(question_id = question.id)
#     tags = list(question.tag.all())
#     context = {
#         "question": question,
#         "answers":answers,
#         "tags":tags,
#     }
#     return render(request, 'blog/question_detail.html',context )    
#///////////////////QuestionDetial/////////////////////////////

#///////////////////AllCategories////////////////////////

