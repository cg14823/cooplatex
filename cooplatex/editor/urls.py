"""Url routes for editor app"""
from django.conf.urls import url
from . import views

app_name = 'editor'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signout/', views.sign_out, name='signout'),
    url(r'^(?P<ownerID>[0-9]+)/(?P<projectName>[a-zA-Z][0-9a-zA-Z_]+)/compile/', views.compile_project, name='compile'),
    url(r'^(?P<ownerID>[0-9]+)/(?P<projectName>[a-zA-Z][0-9a-zA-Z_]+)/save/', views.save_project, name='save'),
    url(r'^(?P<ownerID>[0-9]+)/(?P<projectName>[a-zA-Z][0-9a-zA-Z_]+)/', views.editor_page, name='editorPage'),
    url(r'^(?P<ownerID>[0-9]+)/(?P<projectName>[a-zA-Z][0-9a-zA-Z_]+)/delete/', views.delete_project, name='delete'),
]