from django.contrib import admin
from django.urls import path
from app.views import *

urlpatterns = [
    path('user_registration',user_registration,name = "user_registration"),
    path('get_user',get_user,name = "get_user"),
    path('refrral_user',refrral_user,name = "refrral_user"),
    
]