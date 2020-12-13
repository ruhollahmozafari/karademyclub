from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django.utils.text import slugify
from clubuser.models import ClubUser
from djrichtextfield.models import RichTextField

# import os
# import sys
from django.conf import settings

class Category (models.Model):
    title = models.CharField(max_length= 20, )
    slug = models.SlugField(blank= True , null=True, default='')
    parent = models.ForeignKey('self', on_delete= models.SET_NULL,  blank=True , null= True ,)#still dont know what it is ?

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

    
class Question(models.Model):
    PUBLISH_STATUS = (
    ('draft', 'draft'),
    ('publish', 'publish')
    ) 
    title = models.CharField(max_length=1000,  )
    slug = models.SlugField(blank= True , null=True, default='')
    user_id = models.ForeignKey("clubuser.ClubUser", on_delete=models.CASCADE )
    body = RichTextField()
    status = models.CharField(max_length=15, choices=PUBLISH_STATUS, default='draft')
    created_date = models.DateTimeField(auto_now_add= True,null = True)
    updated_date = models.DateTimeField(auto_now= True, null =True)
    like_number = models.IntegerField(default=0, null=True ,)
    interest = models.ForeignKey(Category,null=True,  on_delete=models.SET_NULL)# this is the category dont worry about the name
    tag = models.ManyToManyField(Tag)

    class Meta :
        pass
        # add verbose_names later 
        # ordering = ['-updated_date','Category',]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode= True)
        super(Question, self).save(*args, **kwargs)
        super().save(*args, **kwargs)

    def snippet(self):# to only show a small part of the question in the quesitons page not all of it if the quesion is too long
        return self.body[:100] + '...' 

    def __str__(self):
        return self.title
    # def save(self):
        # pass


class Answer(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_id = models.ForeignKey("clubuser.ClubUser" ,  on_delete=models.CASCADE)
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
    



class Like(models.Model):
    pass
#     question_id = models.ForeignKey("Question",null=True, on_delete=models.CASCADE)
#     answer_id = models.ForeignKey(Answer,null =True, on_delete=models.CASCADE)
#     user_id = models.ForeignKey(ClubUser ,  on_delete=models.CASCADE)
    
#     class Meta:
#         unique_together= [['ClubUser', 'Question '], ['ClubUser', 'Answer']]
    
#     def __str__(self):
#         if self.answer_id:
#             return f'{self.user_id} {self.answer_id}'
#         else:
#             return f'{self.user_id} {self.question_id}'
            

        
    