import datetime
import os
import xml.etree.ElementTree as ET

import src.invoice_generator as invoice_generator


def test_generate_invoice():
    user_data = {
        "name": "John",
        "surname": "Smith",
        "mail": "john@smi.th",
        "subscriptions": "bronze"
    }

    invoice_date = datetime.date(year=2023, month=10, day=1)

    filename = invoice_generator.generate_invoice_xml(user_data, date=invoice_date)
    invoice_number = filename[8:-4]

    tree = ET.parse(filename)

    assert tree.find("./invoice-number").text == invoice_number
    assert tree.find("./date").text == str(invoice_date)

    # todo test company data when it is standardized (written in a constants file for example)

    assert tree.find("./client/name").text == "John"
    assert tree.find("./client/surname").text == "Smith"

    assert tree.find("./client/name").text == "John"
    assert tree.find("./client/surname").text == "Smith"
    assert tree.find("./client/mail").text == "john@smi.th"
    assert tree.find("./client/subscriptions").text == "bronze"

    # todo test payment amount when subscriptions' cost is added
    assert tree.find("./payment/due").text == "2023-11-01"

    os.remove(filename)
