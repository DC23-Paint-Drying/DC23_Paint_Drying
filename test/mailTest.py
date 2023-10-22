import src.mail

"""
Test by sending mail to self
"""


def test_send_mail():
    subject = "Subject abcd"
    content = "Some text"
    receiver = src.mail.COMPANY_MAIL  # send to self

    src.mail.SendMail(receiver, subject, content, ['attachment.txt'])
    response = src.mail.ReadMail()

    assert response['subject'] == subject
    assert response['content'] == content
    assert response['sender'] == receiver
