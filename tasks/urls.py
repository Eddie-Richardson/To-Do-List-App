from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task-list'),  # Home route for tasks
    path('add/', views.add_task, name='add-task'),  # Add task route
    path('edit/<int:task_id>/', views.edit_task, name='edit-task'),  # Edit task route
    path('delete/<int:task_id>/', views.delete_task, name='delete-task'),  # Delete task route
    path('register/', views.register, name='register'),  # Registration page route
    path('profile/', views.profile, name='profile'),  # Profile page route
    path('logout/', views.custom_logout, name='logout') # Logout page route
]