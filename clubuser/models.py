from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django.utils.text import slugify
# from blog.models import *

# Create your models here.

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
    interest = models.ManyToManyField("blog.Category" ,)
    # reporting_post = models.ForeignKey(Questions)
    
    class Meta :
        pass

    def __str__(self):
        return f'{self.fname} {self.lname}'

    # def save(self):
        # pass
