from django.apps import AppConfig
import os

class EditorConfig(AppConfig):
    name = 'editor'
    path = os.path.dirname(os.path.realpath(__file__))