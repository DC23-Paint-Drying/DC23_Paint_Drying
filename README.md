# Preparing the environment

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

```

# Generating PDF files

Generating PDF files requires wkhtmltopdf: https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf


# Setting mail
Mail sending needs to have set the environmental variables: COMPANY_MAIL and PASSWORD.
Setting them using Bash:
$Env:COMPANY_MAIL   = "mail"
$Env:PASSWORD     = "xxxx xxxx xxxx xxxx"

# Google Drive
Using GdriveManager requires service account secrets file. Path to it should be passed as CONFIG_FILE_PATH environmental 
variable. If CONFIG_FILE_PATH is not set then app won't use GdriveManager.


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



