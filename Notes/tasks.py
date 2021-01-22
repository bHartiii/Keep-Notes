from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger
from Notes.models import Notes
from datetime import datetime, timedelta

logger = get_task_logger(__name__)


@periodic_task(
    run_every=(crontab(minute='*/24*60')),
    name="delete_trashed_note",
    ignore_result=True
)
def delete_trashed_note():
    notes = Notes.objects.filter(isDelete=True)
    for note in notes:
        if datetime.now() - note.trashedAt.replace(tzinfo=None) > timedelta(days=7):
            note.delete()
            return "Trashed notes are deleted!!!" 
        
    return "Trash check!!!"


@periodic_task(
    run_every=(crontab(minute='*/1')),
    name="send_reminder",
    ignore_result=True
)
def send_reminder():
    notes = Notes.objects.filter(isDelete=False).exclude(reminder=None)
    for note in notes:
        if note.reminder.replace(tzinfo=None) - datetime.now() <= timedelta(seconds=1):
            note.reminder = None
            note.save()
            return note
    return "Reminder checked!!!"