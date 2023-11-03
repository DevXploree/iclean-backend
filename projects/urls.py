from django.urls import path
from .views import ListProjects, create_project, delete_project, update_project, pick_project, ListPickedProjects, ListProjectsWithoutDailyUpdates, close_project, notify_update, all_updates

urlpatterns = [
    path('list_projects/', ListProjects.as_view(), name='list_projects'),
    path('create-project/', create_project, name='create_projects'),
    path('delete-project/<uuid:project_id>/', delete_project, name='delete_project'),
    path('update-project/<uuid:project_id>/', update_project, name='update_project'),
    path('close-project/<str:project_id>/', close_project, name='close_project'),
    
    path('pick-project/<uuid:project_id>/', pick_project, name='pick_project'),
    
    path('list-picked-projects/', ListPickedProjects.as_view(), name='list_picked_projects'),
    path('projects-without-updates/', ListProjectsWithoutDailyUpdates.as_view(), name='list-projects-without-updates'),
    
    path('notify-update/<str:project_id>/', notify_update, name='notify-update'),
    path('all-updates/', all_updates, name='all-updates'),
]
