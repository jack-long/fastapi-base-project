import re
import smtplib
from smtplib import SMTPServerDisconnected
from app.core.config import get_settings


class EmailHelper:

    def __init__(self):
        settings = get_settings()
        self.smtp_username = settings.smtp_username
        self.smtp_password = settings.smtp_password
        self.smtp_host = settings.smtp_host
        self.smtp_port = settings.smtp_port
        self.admin_email = settings.admin_email
        self.api_url = settings.api_url
        self.sender = self.smtp_username

    def send(self, subject: str, body: str, recipient: str | None = None):
        if recipient is None:
            recipient = self.admin_email

        message = f'From: Chest <{self.sender}>\n' \
                  f'To: {recipient}\n' \
                  f'Subject: {subject}\n\n{body}'
        print(f"Send email \n{message}")
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=5) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.sendmail(self.sender, recipient, message)
        except SMTPServerDisconnected as e:
            print("Serer disconnected")
            raise e


def send_new_account_email(recipient: str, activation_link: str):
    helper = EmailHelper()
    subject = "Welcome to Chest"
    body = ("Hi,\n\n"
            f"Click the link to verify your email {activation_link}\n\n"
            "Regards,\nChest Admin")
    helper.send(subject=subject, body=body, recipient=recipient)


def send_reset_pw_link_email(recipient: str, reset_link: str):
    helper = EmailHelper()
    subject = "Reset Your Password"
    body = ("Hi,\n\n"
            f"Open the link to reset your password {reset_link}\n\n"
            "Regards\nChest Admin")
    helper.send(subject, body, recipient)


def is_valid_email(email: str) -> bool:
    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(email_pattern, email) is not None
