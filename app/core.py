from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from os import environ
from flask_jwt_extended import JWTManager
from datetime import timedelta


load_dotenv()
app = Flask(__name__)

database_url = environ.get("DATABASE_URL")
database_name = environ.get("POSTGRES_DB_NAME")
jwt_secret_key = environ.get("JWT_SECRET_KEY")

if database_url == None:
    uri = environ.get("POSTGRES_URI")
    password = environ.get("POSTGRES_PASSWORD")
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:{}@{}/{}".format(password, uri, database_name)
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url.replace("postgres://", "postgresql://")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JSON_SORT_KEYS"] = False
app.config["JWT_SECRET_KEY"] = jwt_secret_key
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

db = SQLAlchemy(app)
jwt = JWTManager(app)
