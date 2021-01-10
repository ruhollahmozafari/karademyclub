from django.contrib import admin
from blog.models import *
from clubuser.models import *

admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Report)
admin.site.register(Tag)
admin.site.register(QuestionComment)
admin.site.register(QuestionViews)
admin.site.register(Notification)

