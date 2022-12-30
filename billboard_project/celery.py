import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'billboard_project.settings')

app = Celery('billboard_project')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'send_weekly_content': {
        'task': 'listings.tasks.weekly_content_update',
        'schedule': crontab(hour=0, minute=29, day_of_week='saturday'),
    }
}

app.autodiscover_tasks()
