# Euchre AI

This is by no means any sort of AI, just a player that vaguely follows the
rules.  
Some day I'll spend some time to make this smarter, for now I just wanted to
make sure the site was playable even when noone lese was playing.  
Eventually we should move the communication between the server and the AI
instance(s) to something like Redis I think. This is till using socketio, only
because that'a what the frontend is using to communicate

## Local Setup
```bash
python -m venv venv && venv/bin/pip install -r requirements.txt
venv/bin/pip install -e ../euchrelib/
cp ../.env.local ./.env && venv/bin/python client.py
```
