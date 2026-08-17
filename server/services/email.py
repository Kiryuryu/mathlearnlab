"""
Email utility — send emails via SMTP (admin notifications, password reset).
"""

import logging
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger(__name__)

SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "")


def send_email(to: str, subject: str, body_html: str):
    """Send an HTML email to an arbitrary recipient via SMTP.

    Never raises — failures are logged so callers (e.g. registration /
    password reset) can proceed without crashing.
    """
    if not to or not SMTP_HOST or not SMTP_USER:
        logger.warning("SMTP not configured or no recipient; skipping email: %s", subject)
        return

    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body_html, "html", "utf-8"))

    try:
        server = smtplib.SMTP_SSL(SMTP_HOST, 465)
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, [to], msg.as_string())
        server.quit()
    except Exception:
        logger.exception("Failed to send email to %s: %s", to, subject)


def send_admin_notification(subject: str, body: str):
    """Send an email notification to the admin."""
    if not ADMIN_EMAIL:
        logger.warning("ADMIN_EMAIL not set; skipping admin notification: %s", subject)
        return
    send_email(ADMIN_EMAIL, subject, body)
