"""Mailing module"""
import os
import smtplib

from dotenv import load_dotenv

load_dotenv()


def send_message(message: str, email: str) -> str:
    """Create SMTP connection and send email."""
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(
                os.getenv("SMTP_USER"),
                os.getenv("SMTP_PASS")
            )
            server.sendmail(
                from_addr=os.getenv("SMTP_USER"),
                to_addrs=email,
                msg=message.encode('utf8')
            )
        return "SUCCESS"
    except Exception as exc:
        return exc
