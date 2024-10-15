import smtplib
from email.message import EmailMessage

from celery import Celery
from config import settings

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery("tasks", broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")


def get_email_template_dashboard(username: str):
    email = EmailMessage()
    email["Subject"] = "log"
    email["From"] = settings.SMTP_USER
    email["To"] = settings.SMTP_USER
    email.set_content(f"<div>Hello, {username}</div>", subtype="html")
    return email


@celery.task
def send_email_report_dashboard(username: str):
    email = get_email_template_dashboard(username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(email)
