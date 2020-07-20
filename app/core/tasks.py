from background_task import background
from django.core.mail import EmailMessage
from django.core.mail import mail_admins


@background
def email_bg(subject: str, body: str, sender: str, destination: list, reply_to: list, headers: dict):
    email = EmailMessage(
        subject, body, sender, destination, reply_to=reply_to, headers=headers
    )
    email.send()


@background
def mail_admins_bg(subject: str, body: str):
    mail_admins(subject, body)
