import email
import imaplib
import smtplib, ssl
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename

from typing import List

COMPANY_MAIL = "kubaprojektyinicinnego@gmail.com"
PASSWORD = "cdcm wrfh nbix unvc"


def SendMail(receiver: str, subject:str, content: str, files: List[str]):
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

    #attach files
    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    #send mail
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(COMPANY_MAIL, PASSWORD)
        server.sendmail(COMPANY_MAIL, receiver, msg.as_string())

def ReadMail():
    """
    function used for automatic testing
    however it doesn't correctly check attachments
    :return:
    """
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(COMPANY_MAIL, PASSWORD)
    mail.select('inbox')

    result, data = mail.search(None, 'UNSEEN')
    mail_ids = data[0]

    id_list = mail_ids.split()
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])

    result, data = mail.fetch(str(latest_email_id), '(RFC822)')

    otp = {}
    otp['subject']= ''
    otp['content']= ''
    otp['sender']= ''
    otp['attachments']= ''

    for response_part in data:
        if isinstance(response_part, tuple):
            # from_bytes, not from_string

            msg = email.message_from_bytes(response_part[1])
            otp['subject'] = msg['Subject']
            otp['content'] = msg.get_payload()[0].get_payload()
            otp['attachments'] = msg.get_payload()[1].get_payload()
            otp['sender'] = msg['from']
            #otp['attachments'] = ''
    return otp
