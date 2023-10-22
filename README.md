# Preparing the environment

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

```

# Setting mail
Mail sending needs to have set the environmental variables: COMPANY_MAIL and PASSWORD.
In pycharm they can be set in "Run Configuration".



# Starting the server

```bash
flask --app src/main run
```

# Running tests
```bash
pytest test/
```



