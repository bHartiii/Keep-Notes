from __future__ import absolute_import, unicode_literals

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KeepNotes.settings')

app = Celery('KeepNotes')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'triggering' : {
        'task': 'Notes.tasks.send_email',
        'schedule': 15,
        'args': ('malibharti5@gmail.com',)
    }
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request : {0!r}'.format(self.request))
