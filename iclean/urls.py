from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('all_users.urls')),
    path('api/project/', include('projects.urls')),
]
