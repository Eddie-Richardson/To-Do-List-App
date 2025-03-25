from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')),  # Link the tasks app
    path('login/', auth_views.LoginView.as_view(template_name='tasks/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
