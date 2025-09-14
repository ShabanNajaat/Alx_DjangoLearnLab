from django.contrib.auth.models import AbstractUser, BaseUserManager, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    
    class Meta:
        permissions = [
            ("can_view", "Can view book"),
            ("can_create", "Can create book"),
            ("can_edit", "Can edit book"),
            ("can_delete", "Can delete book"),
        ]
    
    def _str_(self):
        return self.title
