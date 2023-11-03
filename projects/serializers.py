from rest_framework import serializers
from .models import Project, Updates
from all_users.serializers import SalesPersonsSerializer, InstallationPersonsSerializer

class ProjectSerializer(serializers.ModelSerializer):
    installation_person = InstallationPersonsSerializer()
    sales_person = SalesPersonsSerializer()

    class Meta:
        model = Project
        fields = ('id', 'name', 'desc', 'branch', 'sales_person', 'installation_person', 'already_taken', 'created', 'updated', 'closed')
        
        
class UpdateSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    class Meta:
        model = Updates
        fields = "__all__"