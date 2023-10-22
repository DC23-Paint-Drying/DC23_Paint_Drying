import email
import imaplib
import os
import smtplib
import ssl
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
from typing import List, Dict

COMPANY_MAIL = os.environ.get("COMPANY_MAIL", "")
PASSWORD = os.environ.get("PASSWORD", "")

if COMPANY_MAIL == "":
    print("Environmental variable SERVER_GMAIL not set. Sending mail won't function!")
if PASSWORD == "":
    print("Environmental variable SERVER_GMAIL_PASSWORD not set. Sending mail won't function!")


def send_mail(receiver: str, subject: str, content: str, files: List[str]) -> None:
    """
    function which sends mail to appropriate address

    :param receiver: mail to whom the mail is sent. With domain!
    :param subject: title of the mail
    :param content: the text content of a mail
    :param files: list of paths to files to attach
    """
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"

    msg = MIMEMultipart(content)
    msg['Subject'] = subject
    msg['From'] = COMPANY_MAIL
    msg['To'] = ', '.join(receiver)

    msg.attach(MIMEText(content))

    # attach files
    for f in files or []:
        with open(f, "rb") as file:
            part = MIMEApplication(
                file.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    # send mail
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(COMPANY_MAIL, PASSWORD)
        server.sendmail(COMPANY_MAIL, receiver, msg.as_string())


def read_mail() -> Dict:
    """
    function used for automatic testing.
    for attachments field it returns only single attached file name

    :return: dictionary: 'subject', 'content', 'sender', 'attachments'
    """
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(COMPANY_MAIL, PASSWORD)
    mail.select('inbox')

    result, data = mail.search(None, 'UNSEEN')
    mail_ids = data[0]

    id_list = mail_ids.split()
    latest_email_id = int(id_list[-1])

    result, data = mail.fetch(str(latest_email_id), '(RFC822)')

    output = {'subject': '', 'content': '', 'sender': '', 'attachments': ''}

    for response_part in data:
        if isinstance(response_part, tuple):
            # from_bytes, not from_string

            msg = email.message_from_bytes(response_part[1])
            output['subject'] = msg['Subject']
            output['content'] = msg.get_payload()[0].get_payload()
            output['attachments'] = msg.get_payload()[1].get_payload()
            output['sender'] = msg['from']
    return output
