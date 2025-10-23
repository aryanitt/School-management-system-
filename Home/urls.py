from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls ),
    path('accounts/', include('django.contrib.auth.urls')),  # for login/logout/password management
    path('', include("school.urls")),  # homepage and school app urls
    path('student/', include("student.urls")),  # student app urls
    path('authentication/' , include("home_auth.urls")) , 
    path('teachers/', include("Teacher.urls")),
    path('subjects/', include("subject.urls")),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
