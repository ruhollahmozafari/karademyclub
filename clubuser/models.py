from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django.utils.text import slugify

class ClubUser(models.Model):
    gender_choices={('male','آقا'),('woman','خانم')}

    user = models.OneToOneField(User,default=None, on_delete= models.CASCADE ,)
    profile_image = models.ImageField( null=True ,default = '01.png', blank = True)
    interest = models.ManyToManyField("blog.Category" ,blank= True)
    
    def __str__(self): 
            return str(self.user.get_username)

    
    class Meta :
        pass
    # def save(self):
        # pass
        