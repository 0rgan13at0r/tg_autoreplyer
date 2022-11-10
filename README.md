# Telegram Auto-Replyer

## Description
This application auto reply on the messages from favorite contants if you don't answer for these for 5 minutes.
## Install
```python
# Install with pip
pip3 install -r requirements.txt

# Install with poetry
poetry install
```
---
## Settings
For application you have to editing 'config.yml'
```yaml
version: "0.1.0"
client:
  api_id: # Your API ID
  api_hash: # Your API Hash
  phone_number: # Your phone number
  cloud_password: # Your 2FA password if you have it
user_ids: # Users IDs list
  -
  -
  -
```
> **Note**
>
> 'user_id' is list!!!
---