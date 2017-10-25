"""Models for editor app"""
from django.db import models, IntegrityError
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.validators import RegexValidator

# TODO: create functions for file creation but they will be dependent on how we store files
VALIDATOR = RegexValidator(r'^[a-zA-Z][0-9a-zA-Z_]+$',
    'Must start with a letter and can only contain alphanumeric characters and undeerscores.')

class Project(models.Model):
    """Project class"""
    name = models.CharField(max_length=25, validators=[VALIDATOR])
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(default=timezone.now)
    # url to files it will be in blob storage somewher

    def __str__(self):
        return "Name: {} Owner: <{}> Creation Date: {}".format(self.name, self.owner, self.date_created)

    def add_collaborator(self, user_to_add, user_adding):
        """ Add collaborators to the project
        Returns Permisiondenied if user_adding is not owner
        Return integrityError if project/collaborator already exists"""
        if self.owner != user_adding:
            raise PermissionDenied

        if Collaborations.objects.filter(project=self, #pylint: disable=E1101
            collaborator=user_to_add).exists():
            raise IntegrityError

        return Collaborations.objects.create(project=self,#pylint: disable=E1101
            collaborator=user_to_add)

    def get_collaborators(self):
        """Get all collaborators to this project"""
        return Collaborations.objects.filter(project=self).values('collaborator') #pylint: disable=E1101
    
    def remove_collaborator(self, user_to_remove, owner):
        """ Removes user from collaborators:
        Return true if removed
        Returns false if user was not a collaborator
        return Permission denied if owner is not owner """

        if self.owner != owner:
            # To allow collaborators to leave projects
            if user_to_remove != owner:
                raise PermissionDenied

        if Collaborations.objects.filter(project=self, #pylint: disable=E1101
            collaborator=user_to_remove).exists():
            Collaborations.objects.get(project=self, #pylint: disable=E1101
            collaborator=user_to_remove).delete()
            return True

        return False
            
    class Meta:
        unique_together = (('name', 'owner'))

class Collaborations(models.Model):
    """Collaborations relates project with non owner useres that have access
    to the project"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    collaborator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return "Project:<{}>  Collaborator:<{}>".format(self.project, self.collaborator)

    class Meta:
        unique_together = (('project', 'collaborator'))

class Files(models.Model):
    """ Links projects to the files in blob storage somewhere """
    FILE_TYPE = (
        ('tex', 'LaTeX file'),
        ('bib', 'Bibliography'),
        ('img', 'image'),
        ('other', 'other'),
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    url = models.CharField(max_length=50)
    file_name = models.CharField(max_length=20)
    file_type = models.CharField(max_length=6, choices=FILE_TYPE)
    class Meta:
        unique_together = (('project', 'file_name'))