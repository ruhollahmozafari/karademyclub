from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django.utils.text import slugify
from django.contrib import auth
from PIL import Image

class ClubUser(models.Model):
    gender_choices={('male','آقا'),('woman','خانم')}

    user = models.OneToOneField(User,default=None, on_delete= models.CASCADE ,)
    profile_image = models.ImageField(null=True ,default = 'default.jpeg',upload_to = 'profile_pics')
    interest = models.ManyToManyField("blog.Category" ,blank= True)
    
    def __str__(self): 
            return str(self.user.get_username())
    @property
    def image_url(self):
        if self.profile_image and hasattr(self.profile_image, 'url'):
            return self.profile_image.url
        else:
            return '/static/default.jpeg'
            
    class Meta :
        permissions = (
            ('can_view', 'Can View'),
            ('can_modify', 'Can Modify'),
        )

    def save(self,*args, **kwargs):
        super().save()
        if self.profile_image:
            img = Image.open(self.profile_image.path)
            if img.height > 100 or img.width > 100:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.profile_image.path)
                

