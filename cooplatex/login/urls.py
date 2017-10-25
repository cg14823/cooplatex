"""Url routes for login app"""
from django.conf.urls import url

from . import views
app_name = 'login'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signin/', views.sign_in, name='signIn'),
    url(r'^signup/', views.register, name='register')
]