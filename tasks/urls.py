from django.urls import path
from tasks.views import manager_dashboard,user_dashboard,task_form
urlpatterns = [
    path('manager-dashboard/',manager_dashboard),
    path('user-dashboard/',user_dashboard),
    path('create-task/',task_form),
]
