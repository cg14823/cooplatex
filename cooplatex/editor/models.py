"""Models for editor app"""
import re
from django.db import models, IntegrityError
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver


# TODO: create functions for file creation but they will be dependent on how we store files
VALIDATOR = RegexValidator(r'^[a-zA-Z][0-9a-zA-Z_]+$',
    'Must start with a letter and can only contain alphanumeric characters and undeerscores.')

class Project(models.Model):
    """Project class"""
    name = models.CharField(max_length=25, validators=[VALIDATOR])
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(default=timezone.now)
    main_file = models.CharField(max_length=100, validators=[VALIDATOR], default="")
    compiled = models.PositiveIntegerField(default=0)
    compiled_file= models.CharField(max_length=100, default="")

    def __str__(self):
        return "Name: {} Owner: <{}> Creation Date: {}".format(self.name, self.owner, self.date_created)
    
    def get_files(self):
        return Files.objects.filter(project=self)
    def get_file(self, name):
        return Files.objects.get(project=self, file_name=name)

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
    
    def create_new_file(self, new_file_name):
            """ creates a new file."""
            if (re.match(r'^[a-zA-Z][0-9a-zA-Z_]+[.](?:tex|bib)+$', new_file_name) is not None and len(new_file_name) > 3 
                and len(new_file_name) <= 25):
                if Files.objects.filter(project=self, file_name=new_file_name).exists():
                    raise ValueError
                pre,suff = new_file_name.split(".")

                url = "{}-{}-{}".format(self.owner.id, self.name, new_file_name)
                Files(project=self,url=url, file_name=new_file_name, file_type=suff).save()
                return url

            raise ValueError

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
    url = models.CharField(max_length=100)
    file_name = models.CharField(max_length=100)
    file_type = models.CharField(max_length=6, choices=FILE_TYPE)
    class Meta:
        unique_together = (('project', 'file_name'))


@receiver(post_save, sender=Project)
def create_main_file(sender, instance, created, **kwargs):
    """ Creates main file in database """
    if created:
        fileurl = "{}-{}-main.tex".format(instance.owner.id, instance.name)
        filename = "main.tex"
        f = Files.objects.get_or_create(project=instance, url=fileurl, file_name=filename,
        file_type="tex")