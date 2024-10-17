import smtplib
from celery.schedules import crontab
import redis
import requests
from datetime import timedelta
from email.message import EmailMessage
from fastapi import APIRouter
from celery import Celery

from config import settings

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery(
    "tasks", broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0"
)

celery.conf.beat_schedule = {
    "test": {
        "task": 'tasks.refresh_cash',
        "schedule": timedelta(days=1),
    },
    "crontab": {
        "task": 'tasks.refresh_cash',
        "schedule": crontab(hour=14, minute=5),
    },
    "email_tick": {
        "task": 'tasks.send_email',
        "args": ("from tick", ),
        "schedule": timedelta(minutes=5),
    },
}

@celery.task
def refresh_cash():
    redis.flushdb()
    requests.get('http://127.0.0.1:8000/api/last_trading_dates/?count=10')
    requests.get('http://127.0.0.1:8000/api/get_trading_results/?limit=100&skip=0')
    return True


@celery.task
def send_email_(username: str='Iam'):
    email = get_email_template_dashboard(username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(email)


def get_email_template_dashboard(username: str):
    email = EmailMessage()
    email["Subject"] = "log"
    email["From"] = settings.SMTP_USER
    email["To"] = settings.SMTP_USER
    email.set_content(f"<div>Hello, {username}</div>", subtype="html")
    return email
