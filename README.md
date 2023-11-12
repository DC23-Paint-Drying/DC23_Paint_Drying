# Preparing the environment

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

```

# Generating PDF files

Generating PDF files requires wkhtmltopdf: https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf


# Converting DOCX to PDF

Converting DOCX files to PDF requires LibreOffice: https://www.libreoffice.org/download/download-libreoffice/

LIBREOFFICE environmental variable should be set to LibreOffice soffice/soffice.exe path in order to use PDF convert:
* Default location for Windows: C:\Program Files\LibreOffice\program\soffice.exe
* Default location for Linux: /usr/lib/libreoffice/program/soffice (or just "soffice")


# Setting mail
Mail sending needs to have set the environmental variables: COMPANY_MAIL and PASSWORD.
Setting them using Bash:
$Env:COMPANY_MAIL   = "mail"
$Env:PASSWORD     = "xxxx xxxx xxxx xxxx"




# Starting the server

```bash
flask --app src/main run
```

# Running tests
```bash
python -m pytest test/
```

# Running tests with coverage
```bash
coverage run -m pytest test/ -v -s 
coverage report -m
```

# Generating monthly report
```bash
python src/report/report.py generate [DIRECTORY](optional)
```

