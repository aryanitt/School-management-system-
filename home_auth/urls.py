from django.contrib import admin
from django.urls import path, include
from . views import *


urlpatterns = [
    path('signup/' , signup_view , name = 'signup'),
    path('login/' , login_view , name = 'login'),
    path('forget-password/' , forget_password_view , name = 'forget-password'),
    path('reset-password/<str:token>/' , reset_password_view , name = 'reset-password'),
    path('logout/' , logout_view , name = 'logout'),
   
]


