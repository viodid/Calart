import json

with open("/etc/config.json") as config_file:
    config = json.load(config_file)


SECRET_KEY = config.get("SECRET_KEY")
SENDER_EMAIL = config.get("SENDER_EMAIL")
RECEIVER_EMAIL = config.get("RECEIVER_EMAIL")
PASSWORD = config.get("PASSWORD")
