import src.Mail

"""
Test by sending mail to self
"""


def test_send_mail():
    subject = "Subject abcd"
    content = "Some text"
    receiver = "kubaprojektyinicinnego@gmail.com"  # send to self

    src.Mail.SendMail(receiver, subject, content, ['attachment.txt'])
    response = src.Mail.ReadMail()

    assert response['subject'] == subject
    assert response['content'] == content
    assert response['sender'] == receiver
