from django.contrib import admin
from .models import ProjectManagers, SalesPersons, InstallationPersons

# Register your models here.
admin.site.register(ProjectManagers)
admin.site.register(SalesPersons)
admin.site.register(InstallationPersons)
