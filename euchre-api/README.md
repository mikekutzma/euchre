# Euchre API

The API is built on `aiohttp` and `socketio`, and written in python.

## Local Setup
```bash
python -m venv venv && venv/bin/pip install -r requirements.txt
venv/bin/pip install -e ../euchrelib/
cp ../.env.local ./.env && venv/bin/python euchre.py
```
