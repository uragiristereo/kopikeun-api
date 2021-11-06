from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from os import environ

load_dotenv()
uri = environ.get("POSTGRES_URI")
password = environ.get("POSTGRES_PASSWORD")
databaseName = environ.get("POSTGRES_DB_NAME")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:{}@{}/{}".format(password, uri, databaseName)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
