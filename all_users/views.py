# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User, Group
from .models import SuperuserRequest, ProjectManagers, SalesPersons, InstallationPersons
from .serializers import SuperuserRequestSerializer, ProjectManagersSerializer, SalesPersonsSerializer, InstallationPersonsSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import user_passes_test

# SuperUser Request

@api_view(['POST'])
def superuser_request(request):
    username = request.data.get('username')
    password = request.data.get('password')

    # Check if a user with the same username already exists
    if User.objects.filter(username=username).exists():
        return Response({'message': 'User already exists with this username.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Create a user account
        user = User(username=username)
        user.set_password(password)
        user.save()

        # Create a superuser request
        superuser_request = SuperuserRequest(user=user)
        superuser_request.save()

        return Response({'message': 'User signup request submitted successfully.'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        # Handle other unexpected errors
        return Response({'error': 'An error occurred: ' + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# Super User Approval
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Requires authentication, typically for the previous superuser
@user_passes_test(lambda user: user.is_superuser)
def approve_superuser_request(request, request_id):
    try:
        superuser_request = SuperuserRequest.objects.get(pk=request_id)
        
        user = superuser_request.user
        user.is_superuser = True
        user.save()
        
        superuser_request.is_approved = True
        superuser_request.save()

        return Response({'message': 'Superuser request approved successfully.'}, status=status.HTTP_200_OK)
    except SuperuserRequest.DoesNotExist:
        return Response({'message': 'Superuser request not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    
# Create Project Managers
@permission_classes([IsAuthenticated])
@user_passes_test(lambda user: user.is_superuser)
@api_view(['POST'])
def create_project_manager(request):
    if request.method == 'POST':
        serializer = ProjectManagersSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data.get('user')

            # Create a new user account for the project manager
            user = User.objects.create_user(
                username=user_data['username'],
                password=user_data['password'],
                first_name=user_data.get('first_name', ''),
                last_name=user_data.get('last_name', '')
            )
            user.is_staff = True  # Optional
            user.save()

            # Create the project manager instance with name, branch, and user
            project_manager = ProjectManagers.objects.create(
                user=user,
                branch=serializer.validated_data.get('branch')
            )
            
            project_manager.save()
            group, created = Group.objects.get_or_create(name="Project Managers")
            user.groups.add(group)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
# Create Sales Person
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_sales_person(request):
    if request.method == 'POST':
        is_project_manager = ProjectManagers.objects.filter(user = request.user).first().logged_in
        if is_project_manager != "project_manager":
            return Response({"error": "You are not authorized to create sales person"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = SalesPersonsSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data.get('user')

            # Create a new user account for the project manager
            user = User.objects.create_user(
                username=user_data.get("username"),
                password=user_data.get("password"),
                first_name=user_data.get('first_name', ''),
                last_name=user_data.get('last_name', '')
            )
            user.save()

            # Create the project manager instance with name, branch, and user
            sales_person = SalesPersons.objects.create(
                user=user,
                branch=serializer.validated_data.get('branch')
            )
            
            sales_person.save()
            group, created = Group.objects.get_or_create(name="Sales Persons")
            user.groups.add(group)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
# Create Installation Person
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_installation_person(request):
    if request.method == 'POST':
        is_project_manager = ProjectManagers.objects.filter(user = request.user).first().logged_in
        if is_project_manager != "project_manager":
            return Response({"error": "You are not authorized to create sales person"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = InstallationPersonsSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data.get('user')

            # Create a new user account for the project manager
            user = User.objects.create_user(
                username=user_data.get("username"),
                password=user_data.get("password"),
                first_name=user_data.get('first_name', ''),
                last_name=user_data.get('last_name', '')
            )
            user.save()

            # Create the project manager instance with name, branch, and user
            installation_person = InstallationPersons.objects.create(
                user=user,
                branch=serializer.validated_data.get('branch')
            )
            
            installation_person.save()
            group, created = Group.objects.get_or_create(name="Installation Persons")
            user.groups.add(group)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @user_passes_test(lambda user: ProjectManagers.objects.filter(user=user).exists())
def store_push_token(request):
    if request.method == 'POST':
        user = request.user 
        # Get the Expo Push Token from the request data
        expo_push_token = request.data.get('expo_push_token')

        if expo_push_token is None:
            return Response({'error': 'Expo Push Token is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Store the Expo Push Token for the Project Manager
        project_manager = ProjectManagers.objects.filter(user = request.user).first()
        project_manager.push_token = expo_push_token
        project_manager.save()

        return Response({'message': 'Expo Push Token stored successfully'}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    if(ProjectManagers.objects.filter(user = request.user).first()):
        return Response({"user": "project_manager"})
    elif(SalesPersons.objects.filter(user = request.user).first()):
        return Response({"user": "sales_person"})
    elif(InstallationPersons.objects.filter(user = request.user).first()):
        return Response({"user": "installation_person"})
    else:
        return Response({"user": "superuser"})
