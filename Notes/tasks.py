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
            return "Trashed notes are deleted!!!" 


@shared_task()
def send_reminder():
    notes = Notes.objects.filter(isDelete=False).exclude(reminder=None)
    for note in notes:
        if note.reminder.replace(tzinfo=None) - datetime.now() <= timedelta(seconds=1):
            note.reminder = None
            note.save()
            return note