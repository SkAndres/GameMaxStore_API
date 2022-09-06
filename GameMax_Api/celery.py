import os
from celery import Celery
from celery.schedules import crontab
from tzlocal import get_localzone
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GameMax_Api.settings')
app = Celery('GameMax_Api')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.update(timezone=get_localzone())


app.conf.beat_schedule = {
    'check-every-hour': {
        'task': 'api.tasks.cleaning_of_unverified_users',
        'schedule': crontab(hour=1)
    }
}
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
