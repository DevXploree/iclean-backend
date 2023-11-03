from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('create-superuser/', views.create_superuser, name='create_superuser'),
    # path('approve-superuser-request/<str:request_id>/', views.approve_superuser_request, name='approve_superuser_request'),
    path('create-project-manager/', views.create_project_manager, name='create_project_manager'),
    path('create-sales-person/', views.create_sales_person, name='create_sales_person'),
    path('create-installation-person/', views.create_installation_person, name='create_installation_person'),
    
    # Store pushnotification token
    path('store-push-token/', views.store_push_token, name='push-token'),
    # Authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', views.profile, name='profile'),
]

# localhost:8000/api/user/request-superuser/
# localhost:8000/api/user/approve-superuser-request/<str:request_id>/
# localhost:8000/api/user/create-project-manager/
# localhost:8000/api/user/create-sales-person/
# localhost:8000/api/user/create-installation-person/
# localhost:8000/api/user/token/
# localhost:8000/api/user/token/refresh/