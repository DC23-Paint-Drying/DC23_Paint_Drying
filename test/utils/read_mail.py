import email
import imaplib

from mail import COMPANY_MAIL, PASSWORD


def read_mail() -> dict:
    """
    function used for automatic testing.
    for attachments field it returns only single attached file name
    :return: dictionary: 'subject', 'content', 'sender', 'attachments'
    """
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(COMPANY_MAIL, PASSWORD)
    mail.select('inbox')

    data = mail.search(None, 'UNSEEN')
    mail_ids = data[0]

    id_list = mail_ids.split()
    latest_email_id = int(id_list[-1])

    result, data = mail.fetch(str(latest_email_id), '(RFC822)')

    output = {'subject': '', 'content': '', 'sender': '', 'attachments': ''}

    for response_part in data:
        if isinstance(response_part, tuple):
            # from_bytes, not from_string

            # pylint: disable=unsubscriptable-object
            msg = email.message_from_bytes(response_part[1])
            # pylint: enable=unsubscriptable-object
            output['subject'] = msg['Subject']
            output['content'] = msg.get_payload()[0].get_payload()
            output['attachments'] = msg.get_payload()[1].get_payload()
            output['sender'] = msg['from']
    return output
