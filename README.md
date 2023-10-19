# Preparing the environment

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt

```

# Starting the server

```bash
flask --app src/main run
```

# Running tests
```bash
pytest test/
```
