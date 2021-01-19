from __future__ import absolute_import, unicode_literals
from celery import shared_task
import time
from Notes.models import Notes
from datetime import datetime, timedelta


@shared_task()
def delete_trashed_note():
    notes = Notes.objects.filter(isDelete=True)
    for note in notes:
        if datetime.now() - note.trashedAt.replace(tzinfo=None) > timedelta(days=7):
            note.delete()

# @shared_task
# def send_email(email):
#     print(f'A sample msg is sent to {email}')