from django.apps import AppConfig
import os

class LoginConfig(AppConfig):
    name = 'login'
    path = os.path.dirname(os.path.realpath(__file__))