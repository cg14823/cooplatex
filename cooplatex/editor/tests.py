"""Tests for project related objects"""
from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import PermissionDenied
from django.db import transaction
from login.models  import CustomUser
from .models import Project, Collaborations

class ProjectTestCase(TestCase):
    def setUp(self):
        """Setup test environment"""
        self.user = CustomUser.objects.create_user("carlos@carlos.com", "password1")

    def test_project_creation(self):
        """ Test project creation """
        # valid creation
        self.user.create_project("projectname")
        project = Project.objects.get(name="projectname")
        self.assertIsInstance(project, Project)

        # duplicate project creation
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.user.create_project("projectname")

        # invalid name project creation 1
        with self.assertRaises(ValueError):
            with transaction.atomic():
                self.user.create_project("project name")


        # invalid name project creation 2
        with self.assertRaises(ValueError):
            with transaction.atomic():
                self.user.create_project("projectname!")

    def test_get_owned_projects(self):
        """ Test getting projects owned by a user """
        self.user.create_project("projectname")
        projects = self.user.get_my_projects()
        self.assertEqual(projects.count(), 1)

    def test_add_project_collaborators(self):
        """ Test adding collaborators """
        self.user.create_project("projectname")
        project = Project.objects.get(name="projectname")
        user2 = CustomUser.objects.create_user("carlos@gmail.com", "password1")
        user3 = CustomUser.objects.create_user("carlos1@gmail.com", "password1")

        # Add collaborator to project
        project.add_collaborator(user2, self.user)
        group = Collaborations.objects.get(project=project)
        self.assertEqual(group.collaborator, user2)

        # Retrieve collaborators
        project.add_collaborator(user3, self.user)
        group = Collaborations.objects.filter(project=project).values('collaborator')
        collaborators = project.get_collaborators()
        self.assertEqual(len(collaborators), 2)
        self.assertEqual(list(group), list(collaborators))

    def test_retrieve_and_remove_project_collaborator(self):
        """ Test retrieving collaborators """
        self.user.create_project("projectname")
        user2 = CustomUser.objects.create_user("carlos@gmail.com", "password1")
        user3 = CustomUser.objects.create_user("carlos1@gmail.com", "password1")

        project = Project.objects.get(name="projectname")
        
        # Add collaborator to project
        project.add_collaborator(user2, self.user)
        project.add_collaborator(user3, self.user)

        # Retrieve collaborators
        group = Collaborations.objects.filter(project=project).values('collaborator')
        collaborators = project.get_collaborators()
        self.assertEqual(len(collaborators), 2)
        self.assertEqual(list(group), list(collaborators))

        # Remove collaborator
        project.remove_collaborator(user2, self.user)
        collaborators = project.get_collaborators()
        self.assertEqual(len(collaborators), 1)

        # Remove myself
        project.remove_collaborator(user3, user3)
        collaborators = project.get_collaborators()
        self.assertEqual(len(collaborators), 0)

    def test_collaborator_add_remove_permission(self):
        """ Check that only the owner can add and that 
        only the owner or own collaborator can remove."""
        self.user.create_project("projectname")
        user2 = CustomUser.objects.create_user("carlos@gmail.com", "password1")
        user3 = CustomUser.objects.create_user("carlos1@gmail.com", "password1")

        project = Project.objects.get(name="projectname")

        # Try to add with no access to project
        with self.assertRaises(PermissionDenied):
            with transaction.atomic():
                project.add_collaborator(user2, user2)
        
        collaborators = project.get_collaborators()
        self.assertEqual(len(collaborators), 0)

        project.add_collaborator(user2, self.user)
        # Try to remove with no access to project
        with self.assertRaises(PermissionDenied):
            with transaction.atomic():
                project.remove_collaborator(user2, user3)

        collaborators = project.get_collaborators()
        self.assertEqual(len(collaborators), 1)