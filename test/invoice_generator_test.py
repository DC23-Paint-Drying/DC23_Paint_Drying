import datetime
import os
import pytest
import xml.etree.ElementTree as ET

from PyPDF2 import PdfReader

import src.invoice_generator as invoice_generator


def test_generate_invoice():
    user_data = {
        "name": "John",
        "surname": "Smith",
        "mail": "john@smi.th",
        "subscription": "bronze",
        "packages": [
            ["Paint+", 29.99]
        ]
    }

    invoice_date = datetime.date(year=2023, month=10, day=1)

    invoice = invoice_generator.Invoice(user_data, date=invoice_date)
    filename = "invoice-test.xml"

    invoice.save_xml(filename)

    tree = ET.parse(filename)

    assert tree.find("./invoice-number").text == invoice.invoice_number
    assert tree.find("./date").text == str(invoice_date)

    # todo test company data when it is standardized (written in a constants file for example)

    assert tree.find("./client/name").text == "John"
    assert tree.find("./client/surname").text == "Smith"

    assert tree.find("./client/name").text == "John"
    assert tree.find("./client/surname").text == "Smith"
    assert tree.find("./client/mail").text == "john@smi.th"
    assert tree.find("./client/subscription/type").text == "bronze"
    assert tree.find("./client/subscription/cost").text == str(invoice.client_subscription_cost)
    assert tree.find("./client/packages/package/type").text == "Paint+"
    assert tree.find("./client/packages/package/cost").text == "29.99"

    assert tree.find("./payment/due").text == "2023-11-01"
    assert tree.find("./payment/amount").text == str(invoice.total_cost)

    os.remove(filename)


# requires the user to have wkhtmltopdf installed, otherwise raises: OSError: No wkhtmltopdf executable found: "b''"
@pytest.mark.skip(reason="Shouldn't be run automatically")
def test_generate_pdf():
    user_data = {
        "name": "John",
        "surname": "Smith",
        "mail": "john@smi.th",
        "subscription": "bronze",
        "packages": [
            ["Paint+", 29.99]
        ]
    }

    invoice_date = datetime.date(year=2023, month=10, day=1)

    invoice = invoice_generator.Invoice(user_data, date=invoice_date)
    filename = "invoice-test.pdf"

    invoice.save_pdf(filename)

    reader = PdfReader(filename)
    page = reader.pages[0]

    words = []
    for line in page.extract_text().split('\n'):
        for word in line.split(' '):
            words.append(word)

    for word in words:
        print(word)

    assert f"{invoice.invoice_number}" in words
    assert str(invoice_date) in words

    # todo test company data when it is standardized (written in a constants file for example)

    assert "John" in words
    assert "Smith" in words
    assert "john@smi.th" in words

    assert "bronze" in words
    assert str(invoice.client_subscription_cost) in words

    assert "Paint+" in words
    assert "29.99" in words

    assert str(invoice.total_cost) in words

    assert "2023-11-01" in words

    os.remove(filename)
