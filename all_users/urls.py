from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('user_signup/', views.superuser_request, name='superuser_request'),
    path('approve_superuser_request/<int:request_id>/', views.approve_superuser_request, name='approve_superuser_request'),
    path('create-project-manager/', views.create_project_manager, name='create_project_manager'),
    path('create-sales-person/', views.create_sales_person, name='create_sales_person'),
    path('create-installation-person/', views.create_installation_person, name='create_installation_person'),
    
    # Authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
