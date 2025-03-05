import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'csv_processor.settings')

app = Celery('csv_processor')

#app.conf.enable_utc=False
#app.conf.update(timezone='Asia/Kolkata')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'request:{self.request!r}')