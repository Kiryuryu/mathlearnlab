"""
Email utility — send notification emails via SMTP.
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "")


def send_admin_notification(subject: str, body: str):
    """Send an email notification to the admin."""
    if not SMTP_HOST or not SMTP_USER:
        return

    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = ADMIN_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "html", "utf-8"))

    try:
        server = smtplib.SMTP_SSL(SMTP_HOST, 465)
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, [ADMIN_EMAIL], msg.as_string())
        server.quit()
    except Exception:
        pass  # non-critical
