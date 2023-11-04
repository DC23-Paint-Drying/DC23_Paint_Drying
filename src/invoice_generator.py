import datetime
import importlib.resources
import uuid
from dataclasses import dataclass, asdict

import jinja2
import pdfkit

from . import manifest


@dataclass
class Invoice:
    client_name: str
    client_surname: str
    client_mail: str
    client_subscription: str
    client_subscription_cost: float
    client_packets: list[tuple[str, float]]
    total_cost: float
    invoice_date: datetime.date
    payment_due: datetime.date
    company_name: str = manifest.COMPANY_NAME
    company_address: str = manifest.COMPANY_ADDRESS
    company_nip: str = manifest.COMPANY_NIP
    company_bank_account: str = manifest.COMPANY_BANK_ACCOUNT
    invoice_number: str = uuid.uuid4().hex

    def __init__(self, client_data: dict, date: datetime.date | None = None) -> None:
        """
        Creates the Invoice dataclass object.
        The invoice payment is due to the first day of the next month, relative to the invoice's date.

        :param client_data: Data of the client for whom the invoice is to be generated. Must contain fields:
            "name", "surname", "mail", "subscription", "packets".
        :param date: Date of the invoice. If left as None, current date is used.
        """

        self.invoice_date = date
        if self.invoice_date is None:
            self.invoice_date = datetime.datetime.now().date()

        self.payment_due = datetime.date(year=self.invoice_date.year, month=self.invoice_date.month+1, day=1)

        self.client_name = client_data["name"]
        self.client_surname = client_data["surname"]
        self.client_mail = client_data["mail"]
        self.client_subscription = manifest.SUBSCRIPTIONS[client_data["subscription"]]["name"]
        self.client_subscription_cost = manifest.SUBSCRIPTIONS[client_data["subscription"]]["price"]
        self.client_packets = [(manifest.PACKETS[packet]["name"], manifest.PACKETS[packet]["price"]) for packet in client_data["packets"]]

        self.total_cost = self.client_subscription_cost + sum([packet[1] for packet in self.client_packets])

    def save_xml(self, output_filename: str) -> None:
        """
        Saves the Invoice as an XML file with the given name.

        :param output_filename: name of the XML file to be created
        """
        rendered_template = self._render_template("xml_template.xml.j2")

        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write(rendered_template)

    def save_pdf(self, output_filename):
        """
        Saves the Invoice as a PDF file with the given name.

        :param output_filename: name of the PDF file to be created
        """
        rendered_template = self._render_template("pdf_template.html.j2")
        pdfkit.from_string(rendered_template,
                           output_filename,
                           css=importlib.resources.files('src.templates.invoices').joinpath("invoice.css"),
                           options={"enable-local-file-access": True})

    def _render_template(self, template_file: str) -> str:
        """
        Renders the Jinja template in template_file with data taken from the invoice and returns the rendered result.

        :param template_file: filename of the jinja template file
        :return: rendered jinja template
        """
        with importlib.resources.files('src.templates.invoices').joinpath(template_file).open('r', encoding='utf-8') as file:
            template = file.read()

        return jinja2.Template(template).render(**asdict(self))


def generate_invoice_xml(client_data: dict, date: datetime.date | None = None, indent: str = "    ") -> str:
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
    warn("Method generate_invoice_xml() is deprecated. "
         "Please use Invoice(client_data, date).save_xml(output_filename) instead.")

    invoice = Invoice(client_data, date)

    filename = f"invoice-{invoice.invoice_number}.xml"
    invoice.save_xml(filename)

    return filename
