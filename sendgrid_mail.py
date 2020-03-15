from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from config import SENDGRID_KEY, FROM_EMAIL


def send_email(email: str, content: str):
    resp = {}
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=email,
        subject='RSS',
        html_content=content)
    sg = SendGridAPIClient(SENDGRID_KEY)
    response = sg.send(message)
    resp['status_code'] = response.status_code
    resp['body'] = response.body
    resp['header'] = response.headers
    resp['content'] = message.content
    return resp
