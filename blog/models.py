from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django.utils.text import slugify
from clubuser.models import ClubUser
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.conf import settings
from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation
from six import python_2_unicode_compatible
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType



class Category (models.Model):
    title = models.CharField(max_length= 20, )
    slug = models.SlugField(blank= True , null=True, default='')
    parent = models.ForeignKey('self', on_delete= models.SET_NULL,  blank=True , null= True ,)#still dont know what it is ?

    class Meta:
        pass
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

@python_2_unicode_compatible
class Question(models.Model):
    title = models.CharField(max_length=1000,  )
    slug = models.SlugField(blank= True , null=True, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    body = RichTextField(blank= True , null=True)
    published = models.BooleanField(default=True, )
    created_date = models.DateTimeField(auto_now_add= True,null = True)
    updated_date = models.DateTimeField(auto_now= True, null =True)
    like= models.ManyToManyField(User,related_name= 'like_question')
    category = models.ForeignKey(Category,null=True,  on_delete=models.SET_NULL)# this is the category dont worry about the name
    tag = models.ManyToManyField(Tag, blank= True)
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')
    

    class Meta :
        ordering = ['created_date']
        # add verbose_names later 

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode= True)
        super(Question, self).save(*args, **kwargs)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    # def save(self):
        # pass



class Answer(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE, related_name= 'anwers_of_question')
    user = models.ForeignKey(User ,default= None ,null =True, on_delete=models.CASCADE)
    body = body = RichTextField()
    published = models.BooleanField(default=True, )
    created_date = models.DateTimeField(auto_now_add= True,)
    updated_date = models.DateTimeField(auto_now= True)
    like =models.ManyToManyField(User,related_name='like_answer')
    

    class Meta :
        pass
    # add verbose_names later 
        # ordering= ['total_like']

    def __str__(self):
        return self.body


class Report(models.Model):
    REPORT_REASONS = (
        ("not related to programing" ,"not related to programing"),
        ("insulting","insulting"),
        ("sexual content",'sexual content'),
        ("wrong answer","wrong answer"),
        ("inappropriate","inappropriate"),
        ("other","other"),
    )
    reporter = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    content_type = models.ForeignKey(ContentType,on_delete= models.CASCADE, default= None)
    object_id = models.PositiveIntegerField(default = None)
    content_object = GenericForeignKey('content_type', 'object_id')
    detail = models.CharField(max_length=200, null= True , blank = True, default ='')
    reason = models.CharField(max_length=35, choices=REPORT_REASONS, default='publish')
    report_date = models.DateTimeField(auto_now_add= True , null= True)

    def __str__(self):
        return str(self.content_object)
    
class QuestionComment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    question = models.ForeignKey(Question,null= True ,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add= True)
    body = models.CharField(max_length=200, null= True , blank = True, default ='')
    def __str__(self):
        return str(self.body)



