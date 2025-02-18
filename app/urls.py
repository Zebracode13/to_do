from django.urls import path, include  
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path("", views.Homepage.as_view(), name="home"),
    path("task/complete/<int:task_id>/", views.complete_task, name="complete_task"),
    path("task/delete/<int:task_id>/", views.delete_task, name="delete_task"),
    path("task/update/<int:task_id>/", views.update_task, name="update_task"),
    
    # Authentication URLs
    path("accounts/login/", auth_views.LoginView.as_view(template_name='accounts/login.html'), name="login"),
    path("accounts/signup/", views.SignupView.as_view(), name="signup"),  # Updated Signup view
    path("accounts/logout/", views.custom_logout, name="logout"),  # Custom logout function
]

