import src.mail

"""
Test by sending mail to self
"""


def test_send_mail():
    subject = "Subject abcd"
    content = "Some text"
    receiver = src.mail.COMPANY_MAIL  # send to self

    src.mail.send_mail(receiver, subject, content, ['attachment.txt'])
    response = src.mail.read_mail()

    assert response['subject'] == subject
    assert response['content'] == content
    assert response['sender'] == receiver
