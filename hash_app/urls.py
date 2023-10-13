from django.contrib import admin
from django.urls import path, include
from .views import Usersignup, Login


urlpatterns = [
    path('signup/',Usersignup.as_view()),
    path('login/',Login.as_view())
]
