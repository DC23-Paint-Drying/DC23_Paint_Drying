import datetime
import uuid

import jinja2



if __name__ == "__main__":
    with open("./templates/invoices/pdf_template.html", 'r', encoding='utf-8') as file:
        pdf_template = file.read()

    client_data = {
        "name": "John",
        "surname": "Smith",
        "mail": "john@smi.th",
        "subscription": "bronze"
    }

    template = jinja2.Template(pdf_template)
    data = {
        "company_name": "Drying Paint Inc.",
        "company_address": "Paintburg, Paint Street 54/6",
        "company_nip": "123-456-78-90",
        "company_bank_account": "12 3456 7890 0000 0000 1234 5678",
        "client_name": client_data["name"],
        "client_surname": client_data["surname"],
        "client_mail": client_data["mail"],
        "client_subscription": client_data["subscription"],
        "client_subscription_cost": "100 zł",
        "total_cost": "1000 zł",
        "invoice_number": uuid.uuid4().hex,
        "invoice_date": datetime.datetime.now().date(),
        "payment_due": datetime.datetime.now().date(),
        "packages": [
            ["pakiet 1", "100 zł"],
            ["pakiet 2", "200 zł"],
            ["pakiet 3", "300 zł"]
        ]

    }
    rendered = template.render(**data)

    import pdfkit

    pdfkit.from_string(rendered, 'out.pdf', css="./templates/invoices/invoice.css", options={"enable-local-file-access": True})

    #print(rendered)
