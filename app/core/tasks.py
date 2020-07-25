from background_task import background
from django.core.mail import EmailMessage
from django.core.mail import mail_admins
from logging import getLogger

logger = getLogger('tasks')


@background
def email_bg(subject: str, body: str, sender: str, destination: list, reply_to: list, headers: dict):
    email = EmailMessage(
        subject, body, sender, destination, reply_to=reply_to, headers=headers
    )
    try:
        logger.info(
            f'\n'
            f'\n'
            f'Sending mail to {destination} with subject {subject}:\n'
            f'sender: {sender}, reply_to: {reply_to}, body:\n'
            f'{body}\n'
            f'\n'
            f'\n'
        )
        response = email.send()
        logger.info(f'Got Response: {response}')
        if response != 1:
            raise Exception(f'Received response {response} from server')
    except Exception as e:
        logger.error(f'Ecountered error while trying to send email: \n{e}')


@background
def mail_admins_bg(subject: str, body: str):
    mail_admins(subject, body)
