# Create your views here.
from all_users.models import SalesPersons, InstallationPersons, ProjectManagers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import user_passes_test
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User, Group
from .serializers import ProjectSerializer
from .models import Project, Updates
from rest_framework.generics import ListAPIView
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination


@user_passes_test(lambda user: user.groups.filter(name='Sales Persons').exists())
@api_view(['POST'])
def create_project(request):
    if request.method == 'POST':
        # Extract the Sales Person user
        sales_person = request.user

        # Extract data from the request
        data = request.data

        # Create a new project instance and set the sales_person
        project = Project(
            name=data.get('name'),
            desc=data.get('desc'),
            branch=data.get('branch'),
            sales_person=sales_person
        )
        
        # Save the project instance
        project.save()

        return Response({"message": "Project created successfully"}, status=status.HTTP_201_CREATED)

@user_passes_test(lambda user: user.groups.filter(name='Sales Persons').exists())
@api_view(['PUT'])
def update_project(request, project_id):
    try:
        # Retrieve the project based on project_id
        project = Project.objects.get(id=project_id)

        # Check if the Sales Person is the owner of the project
        if project.sales_person != request.user:
            return Response({"message": "You do not have permission to edit this project."}, status=status.HTTP_403_FORBIDDEN)

        # Update the project with the request data
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Project.DoesNotExist:
        return Response({"message": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
    
@user_passes_test(lambda user: user.groups.filter(name='Sales Person').exists())
@api_view(['DELETE'])
def delete_project(request, project_id):
    try:
        # Retrieve the project based on project_id
        project = Project.objects.get(id=project_id)

        # Check if the Sales Person is the owner of the project
        if project.sales_person != request.user:
            return Response({"message": "You do not have permission to delete this project."}, status=status.HTTP_403_FORBIDDEN)

        # Delete the project
        project.delete()

        return Response({"message": "Project deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    except Project.DoesNotExist:
        return Response({"message": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
    
class ListProjects(ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'desc', 'branch']

    # Configure pagination
    pagination_class = PageNumberPagination
    page_size = 10  # Adjust the number of items per page as needed

@user_passes_test(lambda user: user.groups.filter(name='Installation Persons').exists())
@api_view(['PUT'])
def pick_project(request, project_id):
    try:
        # Retrieve the project based on project_id
        project = Project.objects.get(id=project_id)

        # Check if the project is already taken
        if project.already_taken:
            return Response({"message": "This project has already been picked by another Installation Person."}, status=status.HTTP_400_BAD_REQUEST)

        # Assign the project to the current Installation Person
        project.already_taken = True
        project.installation_person = request.user  # Assuming the user model has an installationpersons field
        project.save()

        return Response({"message": "Project picked successfully"}, status=status.HTTP_200_OK)
    except Project.DoesNotExist:
        return Response({"message": "Project not found"}, status=status.HTTP_404_NOT_FOUND)   

class ListPickedProjects(ListAPIView):
    serializer_class = ProjectSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created', 'updated']

    def get_queryset(self):
        # Retrieve and return the projects picked by the current Installation Person
        return Project.objects.filter(installation_person=self.request.user)

@user_passes_test(lambda user: user.groups.filter(name='Installation Persons').exists())    
def send_update(request, project_id):
    if request.method == "POST":
        try:
            project = Project.objects.get(id = project_id)
            if project.installation_person == request.user:
                update_desc = request.data.get("update_desc")
                update = Updates(project = project, update_desc = update_desc)
                update.save()
                return Response({"success": "Successfully delivered the update"}, status=status.HTTP_200_OK)
            else:
                return Response({"failed": "You are not authorized to give update on this project"}, status=status.HTTP_400_BAD_REQUEST)            
        except:
            return Response({"failed": "Project does not exists"}, status=status.HTTP_404_NOT_FOUND) 