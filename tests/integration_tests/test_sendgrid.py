from rss_app.sendgrid_mail import send_email
import pytest


@pytest.mark.xfail()
def test_send_test_mail():
    r = send_email('mail_exeample@example.com', 'hello world')
    assert r['status_code'] == 200
