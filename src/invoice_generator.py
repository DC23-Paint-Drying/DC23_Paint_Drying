from __future__ import annotations

import datetime
import uuid
import xml.etree.cElementTree as ET
from typing import Dict


def generate_invoice_xml(client_data: Dict, date: datetime.date | None = None, indent: str = "    ") -> str:
    """
    Generates an invoice in XML format. Creates a file named "invoice-{invoice_number}.xml" and returns its filename.
    The invoice payment is due to the first day of the next month, relative to the invoice's date.

    :param client_data: Data of the client for whom the invoice is to be generated. Must contain fields:
        "name", "surname", "mail", "subscriptions".
    :param date: Date of the invoice. If left as None, current date is used.
    :param indent: Indentation of the XML file
    :return: Filename of the generated invoice
    """

    if date is None:
        date = datetime.datetime.now().date()

    invoice_number = uuid.uuid4().hex

    invoice = ET.Element("invoice")

    ET.SubElement(invoice, "invoice-number").text = invoice_number

    ET.SubElement(invoice, "date").text = str(date)

    company = ET.SubElement(invoice, "company")
    ET.SubElement(company, "name").text = "Drying Paint Inc."
    ET.SubElement(company, "address").text = "Paintburg, Paint Street 54/6"
    ET.SubElement(company, "NIP").text = "123-456-78-90"
    ET.SubElement(company, "bank-account-number").text = "12 3456 7890 0000 0000 1234 5678"
    # todo maybe get these from a constants file?

    client = ET.SubElement(invoice, "client")
    ET.SubElement(client, "name").text = client_data["name"]
    ET.SubElement(client, "surname").text = client_data["surname"]
    ET.SubElement(client, "mail").text = client_data["email"]
    ET.SubElement(client, "subscriptions").text = client_data["subscriptions"]

    payment = ET.SubElement(invoice, "payment")
    ET.SubElement(payment, "amount").text = "29.99"
    # todo subscriptions cost isn't currently specified
    ET.SubElement(payment, "due").text = str(datetime.date(year=date.year, month=date.month+1, day=1))

    tree = ET.ElementTree(invoice)
    ET.indent(tree, indent)

    filename = f"invoice-{invoice_number}.xml"
    tree.write(filename)

    return filename
