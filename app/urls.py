from django.urls import path
from .views import upload_file, check_task_status

urlpatterns = [
    path('upload/', upload_file, name='upload-file'),
    path('task-status/<str:task_id>/', check_task_status, name='task-status'),
]
