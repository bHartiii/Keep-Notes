from celery import shared_task
import time

@shared_task
def sum(a, b):
    time.sleep(10)
    return a+b

@shared_task
def send_email(email):
    print(f'A sample msg is sent to {email}')