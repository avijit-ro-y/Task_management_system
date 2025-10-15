from django.urls import path
from tasks.views import manager_dashboard,user_dashboard,task_form,view_task,update_task,delete_task
urlpatterns = [
    path('manager-dashboard/',manager_dashboard,name="manager-dashboard"),
    path('user-dashboard/',user_dashboard,name="user-dashboard"),
    path('create-task/',task_form,name='create-task'),
    path('view-task/',view_task),
    path('update-task/<int:id>/',update_task,name='update-task'),
    path('delete-task/<int:id>/',delete_task,name='delete-task'),
]
