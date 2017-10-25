""" Forms for edito app """
from django import forms
from django.core.validators import RegexValidator

VALIDATOR = RegexValidator(r'^[a-zA-Z][0-9a-zA-Z_]+$',
    'Must start with a letter and can only contain alphanumeric characters and undeerscores.')

class ProjectCreateForm(forms.Form):
    """Form for project creation"""
    project_name = forms.CharField(widget=forms.TextInput({
      'required': True,
      'id': 'project-name-input',
      'class': 'form-control',
      'placeholder': 'Title'
    }), max_length=25, min_length=3, validators=[VALIDATOR])