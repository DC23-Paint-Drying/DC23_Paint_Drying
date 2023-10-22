import sys
sys.path.append('src')
import pytest
import mail
from utils.read_mail import read_mail

"""
Test by sending mail to self
"""



@pytest.mark.skip(reason="Shouldn't be run automatically")
def test_send_mail():
    subject = "Subject abcd"
    content = "Some text"
    receiver = mail.COMPANY_MAIL  # send to self

    mail.send_mail(receiver, subject, content, ['attachment.txt'])
    response = read_mail()

    assert response['subject'] == subject
    assert response['content'] == content
    assert response['sender'] == receiver
