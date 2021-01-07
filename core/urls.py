from django.urls import reverse
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from clubuser import views as clubuser_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('blog.urls', namespace='blog')),
    path('',include('clubuser.urls',namespace='clubuser')),
    path('hitcount/', include(('hitcount.urls', 'hitcount'), namespace='hitcount')),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='layouts/password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="layouts/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='layouts/password/password_reset_complete.html'), name='password_reset_complete'),      
    path("password_reset/", clubuser_views.password_reset_request, name="password_reset"),
    
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


