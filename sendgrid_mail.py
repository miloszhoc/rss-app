from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from config import SENDGRID_KEY, FROM_EMAIL


def send_email(email: str, content: str):
    message = Mail(
        from_email=FROM_EMAIL,
        to_emails=email,
        subject='RSS',
        html_content=content)
    try:
        sg = SendGridAPIClient(SENDGRID_KEY)
        response = sg.send(message)
        # print(response.status_code)
        # print(response.body)
        # print(response.headers)
        # print(message.content)
    except Exception as e:
        print(e.message)
