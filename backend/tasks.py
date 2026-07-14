import csv
from io import StringIO
from datetime import date, timedelta
from celery import Celery,shared_task
from celery.schedules import crontab
from flask import current_app
import smtplib
from email.message import EmailMessage
from sqlalchemy import func


from db import db
from models import User, Booking, Trek


def init_celery(flask_app):
    celery_app = Celery(
        flask_app.import_name,
        broker=flask_app.config['CELERY_BROKER_URL'],
        backend=flask_app.config['CELERY_RESULT_BACKEND']
    )
    celery_app.conf.update(
        broker_url=flask_app.config['CELERY_BROKER_URL'],
        result_backend=flask_app.config['CELERY_RESULT_BACKEND'],
        timezone=flask_app.config.get('CELERY_TIMEZONE', 'Asia/Kolkata'),
        broker_connection_retry_on_startup=True
    )

    class ContextTask(celery_app.Task):
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return super().__call__(*args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app

celery = None

def send_email_notification(to_email, subject, body_text, body_html=None, attachments=None):
    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = current_app.config["MAIL_DEFAULT_SENDER"]
    message["To"] = to_email
    message.set_content(body_text)

    if body_html:
        message.add_alternative(body_html, subtype="html")

    for attachment in attachments or []:
        message.add_attachment(
            attachment["content"],
            maintype=attachment.get("maintype", "text"),
            subtype=attachment.get("subtype", "csv"),
            filename=attachment["filename"],
        )

    with smtplib.SMTP(current_app.config["MAIL_SERVER"], current_app.config["MAIL_PORT"]) as smtp:
        if current_app.config.get("MAIL_USE_TLS"):
            smtp.starttls()
        smtp.login(current_app.config["MAIL_USERNAME"], current_app.config["MAIL_PASSWORD"])
        smtp.send_message(message)



#background/scheduled tasks

@shared_task(name="tasks.export_booking_csv")
def export_booking_csv(user_id, recipient_email):
    """User Triggered Async Job: Exports user history to CSV"""
    csv_buffer = StringIO()
    writer = csv.writer(csv_buffer)
    writer.writerow(["User ID", "Trek Name", "Location", "Booking Status", "Start Date"])

    bookings = Booking.query.filter_by(user_id=user_id).all()
    for b in bookings:
        trek = Trek.query.get(b.trek_id)
        writer.writerow([
            user_id,
            trek.title if trek else "Unknown",
            trek.location if trek else "N/A",
            b.status,
            trek.start_date.strftime("%Y-%m-%d") if trek and trek.start_date else ""
        ])

    send_email_notification(
        recipient_email,
        "Your Trekking History Export",
        "Your background CSV export execution is complete. Find your file attached.",
        attachments=[{
            "filename": f"trekking_history_{user_id}.csv",
            "content": csv_buffer.getvalue().encode("utf-8")
        }]
    )
    return {"status": "Completed"}

@shared_task(name="tasks.send_daily_reminders")
def send_daily_reminders():
    """Scheduled Job: Runs daily at 8:00 AM via Celery Beat"""
    today = date.today()
    upcoming_limit = today + timedelta(days=3)
    
    bookings = Booking.query.join(Trek).filter(
        Booking.status == "Booked",
        Trek.start_date >= today,
        Trek.start_date <= upcoming_limit
    ).all()

    for booking in bookings:
        if booking.user and booking.user.email:
            send_email_notification(
                booking.user.email,
                f"Upcoming Trek Reminder: {booking.trek.title}",
                f"Hi {booking.user.username},\nYour trek {booking.trek.title} starts on {booking.trek.start_date}."
            )
    return {"reminders_sent": len(bookings)}



@shared_task(name="tasks.send_monthly_report")
def send_monthly_report():
    """Scheduled Job: Runs monthly on the 1st via Celery Beat"""
    admin = User.query.filter_by(role="admin").first()
    if not admin:
        return {"error": "Admin user missing"}

    completed_count = Trek.query.filter(Trek.status.ilike("completed")).count()
    popular_treks = db.session.query(
        Trek.title, func.count(Booking.id).label("count")
    ).join(Booking).group_by(Trek.id).order_by(func.count(Booking.id).desc()).limit(5).all()

    rows_html = "".join(f"<tr><td>{t[0]}</td><td>{t[1]}</td></tr>" for t in popular_treks)
    
    html_content = f"""
    <h2>Monthly System Activity Report</h2>
    <p>Completed Treks This Month: {completed_count}</p>
    <h3>Top Booked Treks:</h3>
    <table border="1"><tr><th>Trek</th><th>Bookings</th></tr>{rows_html}</table>
    """

    send_email_notification(
        admin.email,
        "Monthly Admin Performance Report",
        "Please find the HTML data summary inside your webview client.",
        body_html=html_content
    )
    return {"status": "Report Sent"}