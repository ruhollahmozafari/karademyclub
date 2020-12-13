
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('blog.urls', namespace='blog')),
    path('user_profile',include('clubuser.urls',namespace='clubuser')),
    path('djrichtextfield/', include('djrichtextfield.urls')), # this is for rich text package
    
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
