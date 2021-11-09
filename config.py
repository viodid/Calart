from os import urandom
import json

with open("/etc/config.json") as config_file:
	config = json.load(config_file)


SECRET_KEY = config.get("SECRET_KEY")
SQLALCHEMY_DATABASE_URI = config.get("SQLALCHEMY_DATABASE_URI")
