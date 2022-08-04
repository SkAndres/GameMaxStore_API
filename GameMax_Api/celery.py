import os
from celery import Celery
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GameMax_Api.settings')
app = Celery(get_asgi_application())
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
