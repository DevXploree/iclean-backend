from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4

# Create your models here.
class ProjectManagers(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.CharField(max_length=200, null=True, blank=True)
    push_token = models.TextField(null=True, blank=True)
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    
    def __str__(self) -> str:
        return self.user.username

class SalesPersons(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.CharField(max_length=200, null=True, blank=True)
    push_token = models.TextField(null=True, blank=True)
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    
    def __str__(self) -> str:
        return self.user.username
    
class InstallationPersons(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    branch = models.CharField(max_length=200, null=True, blank=True)
    push_token = models.TextField(null=True, blank=True)
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    
    def __str__(self) -> str:
        return self.user.username
    
class SuperuserRequest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    push_token = models.TextField(null=True, blank=True)
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)

    def __str__(self):
        return self.user.username

    