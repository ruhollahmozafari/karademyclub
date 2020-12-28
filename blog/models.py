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
    title = models.CharField(max_length=56)
    slug = models.SlugField(blank= True , null=True, default='')
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode= True)
        super(Tag, self).save(*args, **kwargs)
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.title

@python_2_unicode_compatible
class Question(models.Model):
    PUBLISH_STATUS = (
    ('draft', 'draft'),
    ('publish', 'publish')
    ) 
    title = models.CharField(max_length=1000,  )
    slug = models.SlugField(blank= True , null=True, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    body = RichTextField(blank= True , null=True)
    status = models.CharField(max_length=15, choices=PUBLISH_STATUS, default='publish')
    created_date = models.DateTimeField(auto_now_add= True,null = True)
    updated_date = models.DateTimeField(auto_now= True, null =True)
    like= models.ManyToManyField(User,related_name= 'like_question')
    like_number = models.IntegerField(default=0, null=True ,)
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
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_id = models.ForeignKey("clubuser.ClubUser" ,default= None , on_delete=models.CASCADE)
    body = body = models.TextField()
    published = models.BooleanField(default=True, )
    total_like= models.IntegerField(default= 0, null=True)
    created_date = models.DateTimeField(auto_now_add= True,)
    updated_date = models.DateTimeField(auto_now= True)
    

    class Meta :
        pass
    # add verbose_names later 
        # ordering= ['total_like']

    def __str__(self):
        return self.body


class Report(models.Model):
    pass # we still have got to this in tutorials
    # user_id = models.ForeignKey("ClubUser", on_delete=models.CASCADE, verbose_name='reprter', related_name= 'functioner')
    # reported_profile = models.ForeignKey("ClubUser" , null=True, on_delete=models.CASCADE, verbose_name='reported profile')
    # question_id = models.ForeignKey("Question", null = True , on_delete=models.CASCADE)
    # answer_id = models.ForeignKey(Answer, null=True , on_delete = models.CASCADE)
    # reprted_date = models.DateTimeField(auto_now_add= True , null= True)
    


