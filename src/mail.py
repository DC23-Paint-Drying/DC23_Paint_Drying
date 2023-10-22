"""
    Module used for sending and checking mails
"""
import email
import imaplib
import os
import smtplib
import ssl
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
from typing import List

COMPANY_MAIL = os.environ.get("COMPANY_MAIL", "")
PASSWORD = os.environ.get("PASSWORD", "")

if not COMPANY_MAIL:
    print("Environmental variable SERVER_GMAIL not set. Sending mail won't function!")
if not PASSWORD:
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
    for filename in files or []:
        with open(filename, "rb") as file:
            part = MIMEApplication(
                file.read(),
                Name=basename(filename)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="{basename(f)}"'
        msg.attach(part)

    # send mail
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(COMPANY_MAIL, PASSWORD)
        server.sendmail(COMPANY_MAIL, receiver, msg.as_string())
