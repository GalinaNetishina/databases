from fastapi import APIRouter, BackgroundTasks
from tasks.tasks import send_email_report_dashboard


router = APIRouter(prefix="/report")

@router.get('/send')
def get_report(tasks: BackgroundTasks, user='I am'):
    tasks.add_task(send_email_report_dashboard, user)
    return {
        'status': 200,
        'data': 'Message was sended',
        'details': None
    }


# @router.get("/send")
# def get_report(user="I am"):
#     send_email_report_dashboard.delay(user)
#     return {"status": 200, "data": "Message was sended", "details": None}
