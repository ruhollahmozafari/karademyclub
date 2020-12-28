from django.contrib import admin
from blog.models import Category, Question, Answer , Report, Tag
from clubuser.models import *

admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Report)
admin.site.register(Tag)
