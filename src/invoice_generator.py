import datetime
import uuid
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple

import jinja2
import pdfkit


@dataclass
class Invoice:
    client_name: str
    client_surname: str
    client_mail: str
    client_subscription: str
    client_subscription_cost: float
    client_packages: List[Tuple[str, str]]
    total_cost: float
    invoice_date: datetime.date
    payment_due: datetime.date
    company_name: str = "Drying Paint Inc."
    company_address: str = "Paintburg, Paint Street 54/6"
    company_nip: str = "123-456-78-90"
    company_bank_account: str = "12 3456 7890 0000 0000 1234 5678"
    invoice_number: str = uuid.uuid4().hex

    def __init__(self, client_data: Dict, date: datetime.date | None = None) -> None:
        """
        Creates the Invoice dataclass object.
        The invoice payment is due to the first day of the next month, relative to the invoice's date.

        :param client_data: Data of the client for whom the invoice is to be generated. Must contain fields:
            "name", "surname", "mail", "subscription", "packages".
        :param date: Date of the invoice. If left as None, current date is used.
        """

        self.invoice_date = date
        if self.invoice_date is None:
            self.invoice_date = datetime.datetime.now().date()

        self.payment_due = datetime.date(year=self.invoice_date.year, month=self.invoice_date.month+1, day=1)

        self.client_name = client_data["name"]
        self.client_surname = client_data["surname"]
        self.client_mail = client_data["mail"]
        self.client_subscription = client_data["subscription"]
        self.client_subscription_cost = 100  # todo
        self.client_packages = client_data["packages"]

        self.total_cost = self.client_subscription_cost + sum([package[1] for package in self.client_packages])

    def save_xml(self, output_filename: str) -> None:
        """
        Saves the Invoice as an XML file with the given name.

        :param output_filename: name of the XML file to be created
        """
        rendered_template = self._render_template("./templates/invoices/xml_template.xml")

        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write(rendered_template)

    def save_pdf(self, output_filename):
        """
        Saves the Invoice as a PDF file with the given name.

        :param output_filename: name of the PDF file to be created
        """
        rendered_template = self._render_template("./templates/invoices/pdf_template.html")
        pdfkit.from_string(rendered_template,
                           output_filename,
                           css="./templates/invoices/invoice.css",
                           options={"enable-local-file-access": True})

    def _render_template(self, template_file: str) -> str:
        """
        Renders the Jinja template in template_file with data taken from the invoice and returns the rendered result.

        :param template_file: filename of the jinja template file
        :return: rendered jinja template
        """
        with open(template_file, 'r', encoding='utf-8') as file:
            template = file.read()

        return jinja2.Template(template).render(**asdict(self))


def generate_invoice_xml(client_data: Dict, date: datetime.date | None = None, indent: str = "    ") -> str:
    """
    DEPRECATED. Please use Invoice(client_data, date).save_xml(output_filename) instead.

    Generates an invoice in XML format. Creates a file named "invoice-{invoice_number}.xml" and returns its filename.
    The invoice payment is due to the first day of the next month, relative to the invoice's date.

    :param client_data: Data of the client for whom the invoice is to be generated. Must contain fields:
        "name", "surname", "mail", "subscription".
    :param date: Date of the invoice. If left as None, current date is used.
    :param indent: Indentation of the XML file (deprecated, doesn't do anything now)
    :return: Filename of the generated invoice
    """

    from warnings import warn
    warn("Method generate_invoice_xml() is deprecated."
         "Please use Invoice(client_data, date).save_xml(output_filename) instead.")

    invoice = Invoice(client_data, date)

    filename = f"invoice-{invoice.invoice_number}.xml"
    invoice.save_xml(filename)

    return filename
