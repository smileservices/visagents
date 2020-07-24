from background_task import background
from django.core.mail import EmailMessage
from django.core.mail import mail_admins
from logging import getLogger

logger = getLogger(__name__)


@background
def email_bg(subject: str, body: str, sender: str, destination: list, reply_to: list, headers: dict):
    email = EmailMessage(
        subject, body, sender, destination, reply_to=reply_to, headers=headers
    )
    response = email.send()
    logger.info(
        f'==================================================\n'
        f'Sent mail to {destination} with subject {subject}:\n'
        f'sender: {sender}, reply_to: {reply_to}, body:\n'
        f'{body}'
        f'==================================================\n'
        f'response: {response}'
    )


@background
def mail_admins_bg(subject: str, body: str):
    mail_admins(subject, body)
