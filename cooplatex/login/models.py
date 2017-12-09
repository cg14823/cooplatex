"""Models for login app"""
import re
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from editor.models import Project, Collaborations
from .managers import UserManager

# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom user class"""
    email = models.EmailField(max_length=254, unique=True)
    name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    verified = models.BooleanField(default=False)
    verify_token = models.CharField(max_length=40)
    objects = UserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def create_project(self, project_name):
        """ creates a project.
        May raise Value error if project_name is invalid, it may raise
        IntegrityError if project/owner already exist"""
        # TODO: probably create the main file automaticaly
        # TODO: remove 3 character minimum limit on project name (also in corresponding form)
        # First check that project name is valid
        if (re.match(r'^[a-zA-Z][0-9a-zA-Z_]+$', project_name) and len(project_name) > 3 
            and len(project_name) <= 25):
            if Project.objects.filter(owner=self, name=project_name).exists():
                raise ValueError

            Project(name=project_name, owner=self, main_file="{}-{}-main.tex".format(self.id, project_name)).save()
            return

        raise ValueError

    def get_my_projects(self):
        """ Gets projects owned by this user """
        return Project.objects.filter(owner=self)

    def get_shared_with_me(self):
        """ Gets projects id I collaborate in """
        return Collaborations.objects.filter(
            collaborator=self).values_list('project', flat=True)

    def verify(self, token):
        """Verify user"""
        if self.verify_token == token:
            self.verified = True
            self.save()
            return True
        return False
