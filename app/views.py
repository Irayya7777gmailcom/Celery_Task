from django.shortcuts import render

# Create your views here.
import pandas as pd
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import UploadedFile
from .tasks import process_csv_file
from django.core.files.storage import default_storage
from celery.result import AsyncResult

@api_view(['POST'])
def upload_file(request):
    """Handles CSV file upload."""
    print("This api is called")
    file = request.FILES.get('file')
    if not file:
        return JsonResponse({'error': 'No file uploaded'}, status=400)

    uploaded_file = UploadedFile.objects.create(file=file)
    file_path = uploaded_file.file.path
    df = pd.read_csv(file_path)  # Load the CSV
    print(df.columns)
    task = process_csv_file.delay(file_path)  # Celery task
    print("task is=",task)
    return JsonResponse({'message': 'File uploaded successfully', 'task_id': task.id})

@api_view(['GET'])
def check_task_status(request, task_id):
    """Check the status of Celery task."""
    
    print(task_id)
    result = AsyncResult(task_id)
    print(f"Task Status: {result.state}, Result: {result.result}") 
    if result.state == 'FAILURE':
        return JsonResponse({'status': 'FAILURE', 'error': str(result.result)}, status=500)
    return JsonResponse({'status': result.status, 'result': result.result if result.ready() else None})
