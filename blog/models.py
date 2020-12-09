from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django.utils.text import slugify
# import os
# import sys
from django.conf import settings

class Category (models.Model):
    title = models.CharField(max_length= 20, )
    slug = models.SlugField(max_length=20)
    parent = models.ForeignKey('self', on_delete= models.SET_NULL,  blank=True , null= True ,)#still dont know what it is ?


    class Meta :
        pass
    # add verbose_names later 
    #ordering

    def __str__(self):
        return self.title
    # def save(self):
        # pass

class ClubUser(models.Model):
    gender_choices={('male','آقا'),('woman','خانم')}

    fname = models.CharField(max_length= 15,)
    lname= models.CharField(max_length= 15)
    slug= models.SlugField(null=True, blank = True)
    email = models.CharField(max_length=40 ,unique= True)
    gender = models.CharField(null=True, max_length = 10 , choices = gender_choices , )
    sign_up_date= models.DateTimeField(auto_now_add= True, null=True)
    is_active = models.BooleanField(default= True, )
    profile_image = models.ImageField( null=True ,default = '01.png', blank = True)
    interest = models.ManyToManyField(Category ,)
    # reporting_post = models.ForeignKey(Questions)
    
    class Meta :
        pass

    def __str__(self):
        return f'{self.fname} {self.lname}'

    # def save(self):
        # pass


class Question(models.Model):

    title = models.CharField(max_length=1000,  )
    slug = models.SlugField(blank= True , null=True, default='')
    user_id = models.ForeignKey(ClubUser, on_delete=models.CASCADE )
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add= True,null = True)
    updated_date = models.DateTimeField(auto_now= True, null =True)
    like_number = models.IntegerField(default=0, null=True ,)
    interest = models.ManyToManyField(Category)

    class Meta :
        pass
        # add verbose_names later 
        # ordering = ['-updated_date','Category',]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode= True)
        super(Question, self).save(*args, **kwargs)
        super().save(*args, **kwargs)


    def __str__(self):
        return self.title
    # def save(self):
        # pass


class Answer(models.Model):
    question_id = models.ForeignKey("Question", on_delete=models.CASCADE)
    user_id = models.ForeignKey(ClubUser ,  on_delete=models.CASCADE)
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

    # def save(self):
        # pass



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
            

        
    