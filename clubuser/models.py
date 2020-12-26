from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django.utils.text import slugify
from django.contrib import auth

class ClubUser(models.Model):
    gender_choices={('male','آقا'),('woman','خانم')}

    user = models.OneToOneField(User,default=None, on_delete= models.CASCADE ,)
    profile_image = models.ImageField(null=True ,default = 'default.jpeg',upload_to = 'profile_pics' ,blank = True)
    interest = models.ManyToManyField("blog.Category" ,blank= True)
    
    def __str__(self): 
            return str(self.user.get_username())
    @property
    def image_url(self):
        if self.profile_image and hasattr(self.profile_image, 'url'):
            return self.profile_image.url
 
    class Meta :
        pass
