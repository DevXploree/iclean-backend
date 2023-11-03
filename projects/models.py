from django.db import models
from all_users.models import SalesPersons, InstallationPersons
from uuid import uuid4

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField(null=True, blank=True)
    branch = models.CharField(max_length=200, null=True, blank=True)
    sales_person = models.ForeignKey(SalesPersons, blank=True, null=True, related_name="sales_person", on_delete=models.DO_NOTHING)
    installation_person = models.ForeignKey(InstallationPersons, blank=True, null=True, related_name="installation_person", on_delete=models.DO_NOTHING)
    client_name = models.CharField(max_length=200, blank=True, null=True)
    po_quantity = models.IntegerField(null=True, blank=True)
    supplied_quantity = models.IntegerField(null=True, blank=True)
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    already_taken = models.BooleanField(default=False)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    closed = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f"{self.name}"
    
class Updates(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    installed_quatity = models.IntegerField(blank=True, null=True)
    balance_to_be_installed = models.CharField(blank=True, null=True, max_length=300)
    handed_over_quantity = models.IntegerField(blank=True, null=True)
    balance_to_be_handedover = models.CharField(blank=True, null=True, max_length=300)
    update_desc = models.CharField(max_length=600, null = True, blank=True)
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"Update for {self.project.name} - {self.update_desc}"