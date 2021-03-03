from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django.utils.text import slugify
from clubuser.models import ClubUser
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey 
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MinValueValidator, MaxValueValidator



class Report(models.Model):

    REPORT_REASONS = (
        ("not related to programing" ,"not related to programing"),
        ("insulting","insulting"),
        ("sexual content",'sexual content'),
        ("wrong answer","wrong answer"),
        ("inappropriate","inappropriate"),
        ("other","other"),
    )

    #since we have different instances for report we used GenericForeignKey
    #to have only one database (for question, answer, comment, user)
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    content_type = models.ForeignKey(ContentType,on_delete= models.CASCADE, default= None)
    object_id = models.PositiveIntegerField(default = None)
    content_object = GenericForeignKey('content_type', 'object_id')
    detail = models.CharField(max_length=200, null= True , blank = True, default ='')
    reason = models.CharField(max_length=35, choices=REPORT_REASONS, default='publish')
    report_date = models.DateTimeField(auto_now_add= True , null= True)
    active = models.BooleanField(default =True)

    #to make sure and prevent the duplicate report by same person in database
    # (although we managed it in view too )

    class Meta:
        unique_together = ('reporter', 'content_type','object_id')

    def __str__(self):
        return str(self.content_object)


class Category (models.Model):

    title = models.CharField(max_length= 20, )
    slug = models.SlugField(blank= True , null=True, default='')

    class Meta:
        pass
    #to make the slug automatically
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode= True)
        super(Category, self).save(*args, **kwargs)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Tag(models.Model):

    title = models.CharField(max_length=56,null= True)
    slug = models.SlugField(blank= True , null=True, default='')
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode= True)
        super(Tag, self).save(*args, **kwargs)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title

    #to only have the number of post by this past
    def quantity(self):
        return self.question_set.all().count()


class Question(models.Model):


    title = models.TextField(max_length= 255 )
    slug = models.SlugField(blank= True , null=True, default='', max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    body = RichTextField(max_length= 15000,blank= True , null=True)
    active = models.BooleanField(default=True, ) 
    created_date = models.DateTimeField(auto_now_add= True,null = True)
    updated_date = models.DateTimeField(auto_now= True, null =True)
    like= models.ManyToManyField(User,related_name= 'like_question')
    #for like we wont need to make a separate table, django hadles it for us
    category = models.ForeignKey(Category,null=True,  on_delete=models.SET_NULL) 
    tag = models.ManyToManyField(Tag, blank= True)
    reports = GenericRelation(Report ,related_query_name="question")
    #this field helps us to set query having generic relation in reports
    valid_answer = models.ForeignKey("blog.Answer", on_delete=models.CASCADE, null= True,blank=True )
    #the answer that has accepted by the author of the question 

    #fetch the views of the question
    @property
    def views_count(self):
        return QuestionViews.objects.filter(question=self).count()
        
    class Meta :
        ordering = ('-created_date',)
        verbose_name= 'سوال'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode= True)
        super(Question, self).save(*args, **kwargs)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:question-detail",args=[self.pk , str(self.slug)])

    def body_snippets(self):
        return self.body[0:35]

    def title_snippets(self):
        return self.title[0:15]


class QuestionViews(models.Model):

    #to track the views of question based on IP (the same like hitcount)
    IPAddres= models.GenericIPAddressField(default="45.243.82.169")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return '{0} in {1} post'.format(self.IPAddres,self.question.title)


class Answer(models.Model):

    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, related_name= 'anwers_of_question')
    user = models.ForeignKey(User ,default= None ,null =True, on_delete=models.CASCADE)
    body = body = RichTextField()
    active = models.BooleanField(default=True, )
    created_date = models.DateTimeField(auto_now_add= True,)
    updated_date = models.DateTimeField(auto_now= True)
    like =models.ManyToManyField(User,related_name='like_answer')# like question like
    reports = GenericRelation(Report ,related_query_name="answer")

    class Meta :
        pass

    def __str__(self):
        return self.body

    def get_absolute_url(self):
        return reverse("blog:question-detail",args=[self.question_id.pk , str(self.question_id.slug)])


class QuestionComment(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    question = models.ForeignKey(Question,null= True ,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add= True)
    body = models.CharField(max_length=200, null= True , blank = True, default ='')
    reports = GenericRelation(Report ,related_query_name="question_comment")
    #to be able set query for reports we need reports fields in QuesitonComment model
    active = models.BooleanField(default = True)

    def __str__(self):
        return str(self.body)

    def get_absolute_url(self):
        return reverse("blog:question-detail",args=[self.question.pk , str(self.question.slug)])


class Notification(models.Model):

    notification_type = (
        ("question liked" ,"question likedd"),
        ("answer liked","answer liked"),
        ("action reported","action reported"),
        ("question answered","question answered"),
        ("question commented","question commented"),
        ("answer validated","answer validated"),
    )

    user =models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=35, choices= notification_type, default= '', blank = True)
    view = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(4)], default=0)
    # view was declared inorder to track if the notif has read by the user .
    #zero == not read / one == is reading (or delivered)/ two == read
    body = models.CharField(max_length = 500 ,default='', blank = True)
    object = models.ForeignKey(Question, null = True, on_delete=models.CASCADE)
    created_date = models.DateField(auto_now=True)

    #Since all the question, answer, comment are in one signle page(blog:question-detail) the object be > 
    # the question instance to make the redirect easier and also the get_absolute_url goes to related question 
    # also note that in all the view while we are creating a notif the object of instance must be a question instance
    # the profile report will be managed later 
    
    def get_absolute_url(self):
        #in case we dont have the object while saving the notif we dont face error in url
        try :
            return reverse("blog:question-detail", kwargs={"pk": self.object.pk, "slug": self.object.slug})
        except:
            return reverse("blog:questions")

    def __str__(self):
        return self.body
        

class ContactUs(models.Model):

    name = models.CharField(max_length=50, default= '')
    email = models.EmailField(max_length=254, blank=True)
    body = models.TextField( blank = True)

    #it is just to save all contact us form