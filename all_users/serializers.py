from rest_framework import serializers
from .models import ProjectManagers, SalesPersons, InstallationPersons, SuperuserRequest
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'date_joined', 'first_name', 'last_name')

class ProjectManagersSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ProjectManagers
        fields = ('id', 'user', 'branch')

class SalesPersonsSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = SalesPersons
        fields = ('id', 'user', 'branch')

class InstallationPersonsSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = InstallationPersons
        fields = ('id', 'user', 'branch')
        

class SuperuserRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperuserRequest
        fields = '__all__'
