from django.contrib import admin
from django.urls import path, include
from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r'^index/$', views.index, name='index'),
    re_path(r'^$', views.home, name='home'),
    re_path(r'^register/$', views.registration, name='registration'),
    re_path(r'^login/$', views.login_user, name='login'),
    re_path(r'^logout/$', views.logoutUser, name='logout'),
    re_path(r'^mail/$', views.mailBox, name='mailBox'),
]


