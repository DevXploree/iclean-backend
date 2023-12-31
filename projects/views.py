# Create your views here.
from all_users.models import SalesPersons, InstallationPersons, ProjectManagers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProjectSerializer, UpdateSerializer
from .models import Project, Updates
from rest_framework.generics import ListAPIView
from rest_framework import filters, generics
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from exponent_server_sdk import PushClient, PushMessage
from django.shortcuts import get_object_or_404

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_project(request):
    if request.method == 'POST':
        # Extract the Sales Person user
        sales_person = SalesPersons.objects.filter(user = request.user).first()

        # Extract data from the request
        data = request.data
        
        is_sales_person = SalesPersons.objects.filter(user = request.user).first().logged_in
        if is_sales_person != "sales_person":
            return Response({"error": "You are not authorized to create project"}, status=status.HTTP_401_UNAUTHORIZED)

        # Create a new project instance and set the sales_person
        project = Project(
            name=data.get('name'),
            desc=data.get('desc'),
            branch=data.get('branch'),
            client_name=data.get('client_name'),
            po_quantity=data.get('po_quantity'),
            supplied_quantity=data.get('supplied_quantity'),
            sales_person=sales_person
        )
        
        # Save the project instance
        project.save()

        return Response({"message": "Project created successfully"}, status=status.HTTP_201_CREATED)

@permission_classes([IsAuthenticated])
@api_view(['PUT'])
def update_project(request, project_id):
    try:
        is_sales_person = SalesPersons.objects.filter(user = request.user).first().logged_in
        if is_sales_person != "sales_person":
            return Response({"error": "You are not authorized to update project"}, status=status.HTTP_401_UNAUTHORIZED)

        # Retrieve the project based on project_id
        project = Project.objects.get(id=project_id)

        # Check if the Sales Person is the owner of the project
        if project.sales_person != request.user:
            return Response({"message": "You do not have permission to edit this project."}, status=status.HTTP_403_FORBIDDEN)
        
         # Check if the project is already closed
        if project.closed:
            return Response({"message": "This project is closed and further updates are not allowed."}, status=status.HTTP_403_FORBIDDEN)

        # Update the project with the request data
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Project.DoesNotExist:
        return Response({"message": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
    
@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def delete_project(request, project_id):
    try:        
        is_sales_person = SalesPersons.objects.filter(user = request.user).first().logged_in
        if is_sales_person != "sales_person":
            return Response({"error": "You are not authorized to delete project"}, status=status.HTTP_401_UNAUTHORIZED)

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
    
    def get_queryset(self):
        # Filter projects where closed = False
        return Project.objects.filter(closed=False)

@permission_classes([IsAuthenticated])
@api_view(['PUT'])
def pick_project(request, project_id):
    try:
        installation_person = InstallationPersons.objects.filter(user = request.user).first()
        if installation_person.logged_in != "installation_person":
            return Response({"error": "You are not authorized to pick projects"}, status=status.HTTP_401_UNAUTHORIZED)

        # Retrieve the project based on project_id
        project = Project.objects.get(id=project_id)

        # Check if the project is already taken
        if project.already_taken:
            return Response({"message": "This project has already been picked by another Installation Person."}, status=status.HTTP_400_BAD_REQUEST)

        # Assign the project to the current Installation Person
        project.already_taken = True
        project.installation_person = installation_person  # Assuming the user model has an installationpersons field
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
        installation_person = InstallationPersons.objects.filter(user = self.request.user).first()
        return Project.objects.filter(installation_person=installation_person)

@permission_classes([IsAuthenticated])
@api_view(['POST'])
def notify_update(request, project_id):
    try:
        installation_person = InstallationPersons.objects.filter(user = request.user).first()
        if installation_person.logged_in != "installation_person":
            return Response({"error": "You are not authorized to give updates on projects"}, status=status.HTTP_401_UNAUTHORIZED)
        
        project = get_object_or_404(Project, id=project_id)

        if project.installation_person == installation_person:
            update_desc = request.data.get("update_desc")
            installed_quatity = request.data.get("installed_quatity")
            balance_to_be_installed = request.data.get("balance_to_be_installed")
            handed_over_quantity = request.data.get("handed_over_quantity")
            balance_to_be_handedover = request.data.get("balance_to_be_handedover")
            
            # Updates 
            update = Updates(project=project, update_desc=update_desc, installed_quatity = installed_quatity, balance_to_be_installed = balance_to_be_installed, handed_over_quantity = handed_over_quantity, balance_to_be_handedover = balance_to_be_handedover)
            
            update.save()

            # Send a push notification to all project managers
            project_managers = ProjectManagers.objects.all()
            for project_manager in project_managers:
                if project_manager.push_token:
                    try:
                        message = f"Update for project: {project.name}"
                        extra_data = {'update_description': update_desc}
                        response = PushClient().publish(
                            PushMessage(to=project_manager.push_token, body=message, data=extra_data)
                        )
                        response.validate_response()

                    except Exception as exc:
                        # Handle errors (log and handle gracefully)
                        print(exc)

            return Response({"success": "Update delivered and notifications sent to project managers"}, status=status.HTTP_200_OK)
        else:
            return Response({"failed": "You are not authorized to update this project"}, status=status.HTTP_400_BAD_REQUEST)
    except Project.DoesNotExist:
        return Response({"failed": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
    
    
    

class ListProjectsWithoutDailyUpdates(generics.ListAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        # Get the current date in the desired format (e.g., YYYY-MM-DD)
        current_date = timezone.now().date()

        # Filter projects that have no updates for the current date
        return Project.objects.exclude(updates__created__date=current_date).select_related('installation_person')
 
@permission_classes([IsAuthenticated]) 
@api_view(['POST'])   
def close_project(request, project_id):
    try:
        is_project_manager = ProjectManagers.objects.filter(user = request.user).first().logged_in
        if is_project_manager != "project_manager":
            return Response({"error": "You are not authorized to close projects"}, status=status.HTTP_401_UNAUTHORIZED)
        # Retrieve the project based on project_id
        project = Project.objects.get(id=project_id)

        # Check if the project is already closed
        if project.closed:
            return Response({"message": "Project is already closed"}, status=status.HTTP_200_OK)

        # Close the project
        project.closed = True
        project.save()

        return Response({"message": "Project closed successfully"}, status=status.HTTP_200_OK)
    except Project.DoesNotExist:
        return Response({"message": "Project not found"}, status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def all_updates(request):
    try:
        project_manager = ProjectManagers.objects.filter(user = request.user).first()
        if project_manager.logged_in != "project_manager":
            return Response({"error": "You are not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
        updates = Updates.objects.all().order_by("-created")
        serialized_data = UpdateSerializer(updates, many=True).data
        
        return Response(serialized_data)
    except Exception as e:
        return Response({"error":f"{e}"}) 
