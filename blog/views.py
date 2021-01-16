from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse ,reverse_lazy
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse , HttpResponseRedirect
from blog.models import  Answer, Tag , Category, Question, Report
from django.contrib import messages  
from django.utils.decorators import method_decorator
from django.contrib.auth import decorators
from .forms import *
from clubuser.forms import *
from django.views import View
from django.views.generic import ListView,DetailView,UpdateView, DeleteView, CreateView , TemplateView
from hitcount.views import HitCountDetailView
from django.contrib.contenttypes.models import ContentType
from clubuser.models import ClubUser
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count,Min, Max, Avg, Q

class QuestionsList(ListView):
    paginate_by = 5
    template_name = 'blog/question_archive.html'
    queryset = Question.objects.filter(active= True) 


class HomeView(TemplateView):
    template_name = 'blog/home_page.html'


class SearchResultView(ListView):
    model = Question
    template_name = 'blog/search_results.html'
    paginate_by = 5
    context_object_name = 'questions'
    def get_queryset(self):
        self.keyword = self.request.GET.get('keywords', None)
        object_list = Question.objects.filter(Q (title__icontains=self.keyword) 
        | Q(tag__title__icontains = self.keyword) 
        | Q(category__title__icontains = self.keyword )).order_by('-created_date')
        
        return object_list

@login_required
def question_comment(request, *args, **kwargs):
    context ={}
    if request.method == 'POST':
        c_form = QuestionCommentForm(request.POST)
        if c_form.is_valid():        
            new_comment = c_form.save(commit=False)
            question1= Question.objects.get(id = request.POST.get('question_id'))
            new_comment.question = question1
            new_comment.user = request.user
            new_comment.save()
            # sending a notif for user that you got a comment for your question
            Notification.objects.create(
                user = new_comment.user,
                type ='question commented',
                body = f'your question: {new_comment.body[0:50]} received a comment by  {request.user} ',
                object= new_comment.question)

    else:
        context['c_form'] = c_form
    return HttpResponseRedirect(reverse_lazy('blog:question-detail',args=[question1.id , question1.slug]))

@login_required   
def LikeCreate(request, *args, **kwargs):
    object_type = ContentType.objects.get(app_label= kwargs['app'], model = kwargs['model'],)
    real_object = object_type.get_object_for_this_type(id = kwargs['pk'])
    #making a proper id to redirect to question-detail page
    model_name = kwargs['model']
    if model_name == 'answer': # setting id for answer instance 
        id_to_question= real_object.question_id.id
        slug_to_question = real_object.question_id.slug
    else :                      #setting id for question instance
        id_to_question = real_object.id
        slug_to_question = real_object.slug
    #creating a like or if it's liked unlike it 
    if real_object.like.filter(id = request.user.id).exists(): # checking model name to create or delete like for which model
        real_object.like.remove(request.user)

        if model_name == 'question': # checking the model to delete the notif for user
            try:
                Notification.objects.get(
                    user = real_object.user,
                    type ='question liked',
                    body = f'your question: {real_object.body[0:50]} was liked by someone ',
                    object= real_object).delete()
            except:
                pass
        else :
            try:
                Notification.objects.get(
                    user = real_object.user ,
                    type ='answer liked',
                    body = f'your answer: {real_object.body[0:50]} was liked by someone ',
                    object= real_object.question_id).delete()
            except:
                pass

    else:
        real_object.like.add(request.user)
        if model_name == 'question': # checking the model to make a valid notid for user 
            Notification.objects.create(
                user = real_object.user ,
                type ='question liked',
                body = f'your question: {real_object.body[0:50]} was liked by {request.user} ',
                object= real_object)
        else :
            Notification.objects.create(
                user = real_object.user,
                type ='answer liked',
                body = f'your answer: {real_object.body[0:50]} was liked by {request.user} ',
                object= real_object.question_id)

    return HttpResponseRedirect(reverse('blog:question-detail',args = [id_to_question , slug_to_question]))


class QuestionDetail(DetailView):
    template_name = 'blog/question_detail.html'
    model = Question
    context_object_name = 'question'
    def get_client_ip(self, request):
        x_forwarded_for =request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
        
    def get_queryset(self):
        return Question.objects.filter(id = self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_form = QuestionCommentForm()
        context = super(QuestionDetail,self).get_context_data(**kwargs)
        #adding on view based on ip
        QuestionViews.objects.get_or_create(IPAddres=self.get_client_ip(self.request), question=self.object)

        self.obj= get_object_or_404(Question, id = self.kwargs['pk'])
        self.object.save()
        self.object.refresh_from_db()
        answers = Answer.objects.filter (question_id = self.obj.id, active=True).order_by('-created_date')
        liked =self.obj.like.filter(id =self.request.user.id).exists()
        comments= QuestionComment.objects.filter(question = self.kwargs['pk'], active=True)
        context['comments']= comments
        context["answers"]=answers
        context["liked "] = liked
        context['c_form'] = c_form
        return context
        post_details=Post.objects.get(slug=slug)


class AllCategories(ListView):
    model = Category
    template_name = 'blog/all_categories.html'
    context_object_name = 'categories'


class QuestionsInCategories(ListView,): 
    model = Category
    template_name = 'blog/questions_in_categories.html'
    context_object_name = 'questions'
    paginate_by = 5

    
    def get_queryset(self,*args, **kwargs):
        self.cat =get_object_or_404(Category, slug = self.kwargs['slug'])
        return Question.objects.filter(category = self.cat)
    def get_context_data(self, **kwargs):
        context = super(QuestionsInCategories,self).get_context_data(**kwargs)
        context["main_cat"]= self.cat
        return context


class AllTags(ListView):
    model = Tag
    template_name='blog/all-tags.html'
    context_object_name = 'tags'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        most_used_tags= Tag.objects.all().annotate(post_count=Count('question')).order_by('-post_count')[0:10]
        context["most_used_tags"] = most_used_tags
        return context


class QuestionsInTags(ListView):
    model = Tag
    template_name = 'blog/questions-in-tags.html'
    context_object_name = 'questions'
    paginate_by = 5

    def get_queryset(self,):
        self.tag =get_object_or_404(Tag, slug = self.kwargs['slug'])
        return Question.objects.filter(tag = self.tag) 

    def get_context_data(self, **kwargs):
        context = super(QuestionsInTags,self).get_context_data(**kwargs)
        context["main_tag"]= self.tag
        return context


@login_required
def update_question(request, pk ):
    context ={}
    form = UpdateQuestionForm(request.POST)
    instance = Question.objects.get(id = pk)
    if request.method == "POST" and form.is_valid()  :
        instance.title = form.cleaned_data.get('title')
        instance.body = form.cleaned_data.get('body')
        instance.category = form.cleaned_data.get('category')
        tag_list= form.cleaned_data.get('tag_char')
        instance.tag.all().delete() # delete the previous tags in order not to save new ones over the old ones
        tag_list = tag_list.lower().split() 
        for item in tag_list:
            if Tag.objects.filter(title = item).exists():
                temp_tag = Tag.objects.get(title = item)
                instance.tag.add(temp_tag.id)
            else : 
                temp_tag = Tag(title = item)
                temp_tag.save()
                temp_tag.refresh_from_db()
                instance.tag.add(temp_tag.id)    
        instance.save()
        context = { "question": instance}
        return HttpResponseRedirect (reverse_lazy('blog:questions'), context)
    if request.method=='GET':
        tags = instance.tag.all()
        t_char = f''
        for tag in tags: 
            t_char += str(tag) 
            t_char+=' '
        init_title = instance.title
        init_body = instance.body
        init_category = instance.category
        init_tag = t_char

        initial_dict = {
            'title':init_title,
            'body':init_body,
            'category':init_category,
            'tag_char': t_char,
        }

        form = UpdateQuestionForm(
            initial = initial_dict) 
        context['form']= form 
        context['question']= instance
        return render(request, "blog/update_question.html", context) 


@method_decorator(login_required, name = 'dispatch')
class QuestionDelete(DeleteView):
    model =Question
    template_name = 'blog/delete-question.html'
    success_url = reverse_lazy('blog:questions')
            

@method_decorator(login_required, name = 'dispatch')
class QuestionCreate(CreateView):
    def get(self, request ):
        form = Ask()
        return render(request, 'blog/ask.html',{'form': form})

    def post(self, request):
        form = Ask(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            tag_list= form.cleaned_data.get('tag_char')
            tag_list = tag_list.lower().split()
            for item in tag_list:
                if Tag.objects.filter(title = item).exists():
                    temp_tag = Tag.objects.get(title = item)
                    question.tag.add(temp_tag.id)
                else : 
                    temp_tag = Tag(title = item)
                    temp_tag.save()
                    temp_tag.refresh_from_db()
                    question.tag.add(temp_tag.id)

            question.save()
            form= Ask()
            messages.success(request, "Question succesfully created, wait for your answer ")
        return HttpResponseRedirect(reverse_lazy('blog:questions'))


@method_decorator(login_required, name = 'dispatch')
class WriteAnswer(CreateView):
    success_url = reverse_lazy('blog:question')
    def get(self, request , pk):
        form = AnswerForm()
        question_to_answer = get_object_or_404(Question, id = pk)
        context = {
            "form":form,
            "question": question_to_answer,
        }
        return render(request, 'blog/answer-question.html',context)


    def post(self, request,pk):
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.body = form.cleaned_data.get('body')
            answer.question_id = Question.objects.get(id = request.POST.get('question_id'))
            question= get_object_or_404(Question, id = pk)
            answer.save()
            Notification.objects.create(
                user = answer.user ,
                type ='question answered',
                body = f'your question: {answer.question_id.body[0:50]} was answered by {request.user} ',
                object= answer.question_id)

            form = AnswerForm()
            return HttpResponseRedirect(reverse_lazy('blog:question-detail', args=[question.id, question.slug]))


@method_decorator(login_required, name = 'dispatch')
class DeleteAnswer(DeleteView):
    model = Answer
    template_name = 'blog/delete-answer.html'
    # success_
    success_url = reverse_lazy('blog:questions')
    def get_context_data(self,*args, **kwargs): # to delete the notif for created answer in WriteAnswer
        context = super().get_context_data(**kwargs)
        try:
            answer = Answer.objects.get(pk = self.kwargs['pk'])
            Notification.objects.get(
                user = answer.user,
                type ='question answered',
                body = f'your question: {answer.question_id.body[0:50]} was answered by {answer.user} ',
                object= answer.question_id).delete()
        except:
            pass
        return context


@method_decorator(login_required, name = 'dispatch')
class UpdateAnswer(UpdateView):
    model = Answer
    template_name = 'blog/update-answer.html'
    fields = ['body']
    success_url= reverse_lazy('blog:questions')

@method_decorator(login_required, name = 'dispatch')
class UpdateComment(UpdateView):
    model=QuestionComment
    form_class = UpdateCommentFrom
    template_name ='blog/update-comment.html'
    success_url = reverse_lazy('blog:questions')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment = QuestionComment.objects.get(id = self.kwargs['pk'])
        question = comment.question
        # question = Question.objects.get(id = comment.quesiton.id)
        context["question"] = question
        context["comment"] =comment 
        return context
        
@method_decorator(login_required, name = 'dispatch')
class DeleteComment(DeleteView):
    model = QuestionComment
    template_name = 'blog/delete-comment.html'
    success_url = reverse_lazy('blog:questions')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment = QuestionComment.objects.get(id = self.kwargs['pk'])
        question = comment.question
        # deleting the notif for having comment for your question casue it was deleted
        try:
            Notification.objects.get(
                user = comment.user,
                type ='question commented',
                body = f'your question: {comment.body[0:50]} received a comment by  {comment.user} ',
                object= comment.question).delete()
        except:
            pass

        context["comment"] =comment 
        context["question"] = question
        return context
    

@method_decorator(login_required, name = 'dispatch')
class ListReport(ListView):
    template_name = 'blog/all-reports.html'
    context_object_name = 'reports'
    queryset = Report.objects.filter(active= True)
    ordering= ['-report_date']
    paginate_by = 5

def report_detail(request,*args, **kwargs):
    template_name = 'blog/report-detail.html'
    context = {}
    report = get_object_or_404(Report , pk = kwargs['pk'])  
    all_reports = Report.objects.filter(Q(question__id =report.object_id)
                                        | Q(answer__id = report.object_id) 
                                        | Q(question_comment__id= report.object_id) ).exclude(id = report.id)

    numbers = all_reports.count()
    context["main_report"]= report 
    context["all_reports"] = all_reports 
    context["numbers"] = numbers
    return render(request , template_name , context)

class ReportValid(TemplateView):
    template_name = 'blog/report-valid.html'
    succes_url = reverse_lazy('blog:all-reports')
    success_message = "the case successfuly deactived and the notif was send"
    def post(request, *args, **kwargs):
        report = Report.objects.get(pk= kwargs['pk']) # was about to delete it but it is said that the data is priceless so why dont store it
        subject = report.content_object # subject is the casse which has been reported (question, comment, answer), we take it here inorder to deactive that 
        subject.active= False        
        subject.save()

        # sending warning email to the user of the case and tell them the reason for reporting
        subject = f'Your {report.content_type.model} hase been reported'
        html_content = render_to_string('blog/report_mail.html', {'report':report})
        text_content= strip_tags(html_content)
        recepient = str(report.content_object.user.email)
        send_mail(subject, text_content, 'ruhytest@gmail.com', [recepient], fail_silently = True)

        Notification.objects.create(
            user = report.content_object.user ,
            type ='action reported',
            body = f'your action: {report.content_object} was blocked because it was reported by users. if you have problem with this action contant us by the contact us form.')
        all_reports = Report.objects.filter(Q(question__id =report.object_id)
                                            | Q(answer__id = report.object_id) 
                                            | Q(question_comment__id= report.object_id) )

        t = all_reports.count()
        for rpt in all_reports:
            rpt.active = False
            rpt.save()
            Notification.objects.create(
                user = rpt.reporter ,
                type ='action reported',
                body = f'The case that you reported: {report.content_object} helped us to determine an invalid action, thank you dear : {rpt.reporter}',)
        return HttpResponseRedirect(reverse_lazy('blog:all-reports'))


class ReportInValid(TemplateView):
    template_name= 'blog/report-invalid.html'
    success_url = reverse_lazy('blog:all-reports')
    success_message = "the report case was ignored "
    def post(request, *args, **kwargs):
        report = Report.objects.get(pk= kwargs['pk'])
        all_reports = Report.objects.filter(Q(question__id =report.object_id) 
                                            | Q(answer__id = report.object_id) 
                                            | Q(question_comment__id= report.object_id) )
        for rpt in all_reports:
            rpt.active = False
            rpt.save()
        return HttpResponseRedirect(reverse_lazy('blog:all-reports'))


@method_decorator(login_required, name = 'dispatch')
class CreateReport(CreateView):
    template_name = 'blog/create-report.html'
    form_class = ReportForm

    def get(self, request ,*args,**kwargs ):
        form = ReportForm()
        content_type =ContentType.objects.get(app_label= self.kwargs['app'].lower(), model =(self.kwargs['model']).lower())# note that all the app and model name msut be lowercase 
        object_id = self.kwargs['pk']
        if Report.objects.filter(content_type = content_type , object_id = object_id, reporter = request.user).exists():
            return render (request, 'blog/duplicate-report.html')
        else:
            return render(request, 'blog/create-report.html',{'form': form})

    def post(self, request, *args, **kwargs):
        form = ReportForm(request.POST)
        if form.is_valid() or request.user in all_reports :
            report = form.save(commit=False)
            report.reporter = request.user
            report.content_type =ContentType.objects.get(app_label= self.kwargs['app'].lower(), model =(self.kwargs['model']).lower())# note that all the app and model name msut be lowercase 
            report.object_id = self.kwargs['pk']
            report.detail = form.cleaned_data.get('detail')
            report.reason = form.cleaned_data.get('reason')
            report.save()
            # sending a notif for user that you got a comment for your question
            Notification.objects.create(
                    user = report.reporter,
                    type ='action reported',
                    body = f'We have received your report for the case{report.content_object.body[0:15]}, we will dispose it in no time.Thank you for supporting us',)

            form= Ask()
            messages.success(request, "report succesfully created, we will respond to your ")
        return HttpResponseRedirect(reverse_lazy('blog:questions')) 
        

# it seems that we dont this cause we dont delete the report just deactive it but keeping it in case of need
class DeleteReport(DeleteView):
    model = Report
    template_name = 'blog/delete-report.html'
    success_url = reverse_lazy('blog:all-reports')







# from this line on are the the funciotns which was created at first then the whole view was turned to CBV
# kept it for learning and checking later



    # def post(request, *args, **kwargs):# this was for comment section in QuestionDetial which I used an other function to make it happen
    #     print('post started'*100)
    #     c_form = QuestionCommentForm()
    #     if c_form.is_valid():        
    #         new_comment = c_form.save(commit=False)
    #         new_comment.refresh_from_db()
    #         new_comment.user = request.user
    #         new_comment.question = c_form.cleaned_data.get('question_id')
    #         new_comment.bldy =c_form.cleaned_data.get('body')
    #         new_comment.save()
    #         context= {
    #             "c_form":c_form
    #         }
    #     else:
    #         c_form= QuestionCommentForm()
    #         context= {
    #             "c_form":c_form
    #         }
    #     return render(request, 'blog/question_detail.html',context)
        


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



#at first we userd two different functions handle for like for question and answer specifically but then we used one funstions to handle both of them  
# # @method_decorator(login_required, name = 'dispatch')
# def LikeQuestionView(request, pk):
#     question= get_object_or_404(Question, id = request.POST.get('question_id'))
#     if question.like.filter(id = request.user.id).exists():
#         question.like.remove(request.user)
#     else :      
#         question.like.add(request.user)
#     return HttpResponseRedirect(reverse('blog:question-detail', args=[str(pk), question.slug]))

# # @method_decorator(login_required, name = 'dispatch')
# def LikeAnswerView(request, pk):
#     print('enter the def anser like' * 10)
#     answer= get_object_or_404(Answer, id= request.POST.get('answer_id'))
#     print(answer.id * 1000)
#     if answer.like.filter(id = request.user.id).exists():
#         answer.like.remove(request.user)
#     else :
#         answer.like.add(request.user)
#     return HttpResponseRedirect(reverse('blog:question-detail', args=[str(answer.question_id.id), str(answer.question_id.slug)]))
