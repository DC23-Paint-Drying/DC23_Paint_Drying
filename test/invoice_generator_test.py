import datetime
import os
import xml.etree.ElementTree as ET

from PyPDF2 import PdfReader

import src.invoice_generator as invoice_generator
from src import manifest


def test_generate_invoice():
    user_data = {
        "name": "John",
        "surname": "Smith",
        "email": "john@smi.th",
        "subscription": "basic",
        "packets": ["monthly"]
    }

    invoice_date = datetime.date(year=2023, month=10, day=1)

    invoice = invoice_generator.Invoice(user_data, date=invoice_date)
    filename = "invoice-test.xml"

    invoice.save_xml(filename)

    tree = ET.parse(filename)

    assert tree.find("./invoice-number").text == invoice.invoice_number
    assert tree.find("./date").text == str(invoice_date)

    assert tree.find("./company/name").text == manifest.COMPANY_NAME
    assert tree.find("./company/address").text == manifest.COMPANY_ADDRESS
    assert tree.find("./company/NIP").text == manifest.COMPANY_NIP
    assert tree.find("./company/bank-account-number").text == manifest.COMPANY_BANK_ACCOUNT

    assert tree.find("./client/name").text == "John"
    assert tree.find("./client/surname").text == "Smith"

    assert tree.find("./client/name").text == "John"
    assert tree.find("./client/surname").text == "Smith"
    assert tree.find("./client/mail").text == "john@smi.th"
    assert tree.find("./client/subscription/name").text == "Podstawowy"
    assert tree.find("./client/subscription/cost").text == str(invoice.client_subscription_cost)
    assert tree.find("./client/packets/packet/name").text == "Miesięczny"
    assert tree.find("./client/packets/packet/cost").text == "9.99"

    assert tree.find("./payment/due").text == "2023-11-01"
    assert tree.find("./payment/amount").text == str(invoice.total_cost)

    os.remove(filename)


def test_generate_invoice_deprecated():
    user_data = {
        "name": "John",
        "surname": "Smith",
        "email": "john@smi.th",
        "subscription": "basic",
        "packets": ["monthly"]
    }

    invoice_date = datetime.date(year=2023, month=10, day=1)

    filename = invoice_generator.generate_invoice_xml(user_data, date=invoice_date)
    invoice_number = filename[8:-4]

    tree = ET.parse(filename)

    assert tree.find("./invoice-number").text == invoice_number
    assert tree.find("./date").text == str(invoice_date)

    assert tree.find("./company/name").text == manifest.COMPANY_NAME
    assert tree.find("./company/address").text == manifest.COMPANY_ADDRESS
    assert tree.find("./company/NIP").text == manifest.COMPANY_NIP
    assert tree.find("./company/bank-account-number").text == manifest.COMPANY_BANK_ACCOUNT

    assert tree.find("./client/name").text == "John"
    assert tree.find("./client/surname").text == "Smith"

    assert tree.find("./client/name").text == "John"
    assert tree.find("./client/surname").text == "Smith"
    assert tree.find("./client/mail").text == "john@smi.th"
    assert tree.find("./client/subscription/name").text == "Podstawowy"
    assert tree.find("./client/packets/packet/name").text == "Miesięczny"
    assert tree.find("./client/packets/packet/cost").text == "9.99"

    assert tree.find("./payment/due").text == "2023-11-01"

    os.remove(filename)


def test_generate_pdf():
    user_data = {
        "name": "John",
        "surname": "Smith",
        "email": "john@smi.th",
        "subscription": "basic",
        "packets": ["monthly"]
    }

    invoice_date = datetime.date(year=2023, month=10, day=1)

    invoice = invoice_generator.Invoice(user_data, date=invoice_date)
    filename = "invoice-test.pdf"

    invoice.save_pdf(filename)

    page = PdfReader(filename).pages[0]

    words = page.extract_text().split()

    assert f"{invoice.invoice_number}" in words
    assert str(invoice_date) in words

    for w in manifest.COMPANY_NAME.split():
        assert w in words
    for w in manifest.COMPANY_ADDRESS.split():
        assert w in words
    for w in manifest.COMPANY_NIP.split():
        assert w in words
    for w in manifest.COMPANY_BANK_ACCOUNT.split():
        assert w in words

    assert "John" in words
    assert "Smith" in words
    assert "john@smi.th" in words

    assert "Podstawowy" in words
    assert str(invoice.client_subscription_cost) in words

    assert "Miesięczny" in words
    assert "9.99" in words

    assert str(invoice.total_cost) in words

    assert "2023-11-01" in words

    os.remove(filename)
