"""Url routes for editor app"""
from django.conf.urls import url
from . import views

app_name = 'editor'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signout/', views.sign_out, name='signout'),
    url(r'^create/', views.create_porject, name='create-project')
]