from __future__ import absolute_import, unicode_literals

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KeepNotes.settings')

app = Celery('KeepNotes')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.timezone = 'UTC'

app.conf.beat_schedule = {
    'trash':{
        'task':'Notes.tasks.delete_trashed_note',
        'schedule': 24*60*60,
    },
    'reminder':{
        'task':'Notes.tasks.send_reminder',
        'schedule': 5,
    }
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
