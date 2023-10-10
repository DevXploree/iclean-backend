from django.urls import path
from .views import ListProjects, create_project, delete_project, update_project

urlpatterns = [
    path('list_projects/', ListProjects.as_view(), name='list_projects'),
    path('delete_project/<uuid:project_id>/', delete_project, name='delete_project'),
    path('update_project/<uuid:project_id>/', update_project, name='update_project'),
    path('create_project/', create_project, name='update_project'),
]
