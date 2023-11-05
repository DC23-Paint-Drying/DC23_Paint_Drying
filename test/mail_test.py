import pytest

import src.mail
import utils.read_mail
"""
Test by sending mail to self
"""



@pytest.mark.skip(reason="Shouldn't be run automatically")
def test_send_mail():
    subject = "Subject abcd"
    content = "Some text"
    receiver = src.mail.COMPANY_MAIL  # send to self

    src.mail.send_mail(receiver, subject, content, ['attachment.txt'])
    response = utils.read_mail.read_mail()

    assert response['subject'] == subject
    assert response['content'] == content
    assert response['sender'] == receiver
