from django.contrib import admin
from blog.models import ClubUser, Category, Question, Answer , Report, Like

admin.site.register(ClubUser)
admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Report)
admin.site.register(Like)