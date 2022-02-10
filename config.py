import json

with open("/etc/calat33/config.json") as config_file:
    config = json.load(config_file)


SECRET_KEY = config.get("SECRET_KEY")
MAIL_DEFAULT_SENDER = config.get("SENDER_EMAIL")
MAIL_USERNAME = config.get("SENDER_EMAIL")
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_PASSWORD = config.get("PASSWORD")
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 25
