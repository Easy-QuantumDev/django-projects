from django.urls import path 
from .views import *
app_name = 'tasks'
urlpatterns = [
    path("task_list/",task_list,name='home'),
    path("task_detail/<int:pk>",task_detail,name='task_detail'),
    path("create_task/",create_task,name='create_task'),
    path("task_delete/<int:pk>/",delete_task,name='delete_task'),
    path("task_toggle/<int:pk>/",task_toggle,name='toggle_task'),
    path("task_edit/<int:pk>",edit_task,name='edit_task'),
    

    

    
]