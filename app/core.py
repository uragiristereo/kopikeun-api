from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from os import environ

load_dotenv()
app = Flask(__name__)

databaseURL = environ.get("DATABASE_URL")
databaseName = environ.get("POSTGRES_DB_NAME")

if databaseURL == None:
    uri = environ.get("POSTGRES_URI")
    password = environ.get("POSTGRES_PASSWORD")
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:{}@{}/{}".format(password, uri, databaseName)
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = databaseURL

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
