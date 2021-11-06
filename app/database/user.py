from app import db
from enum import Enum


# class Levels(Enum):
#     user = "user"
#     partner = "partner"
#     admin = "admin"


class User(db.Model):
    email = db.Column(db.String(255), primary_key=True)
    hash_ = db.Column(db.String(255), unique=True, nullable=False)
    # level = db.Column(Enum(Levels), nullable=False)
    level = db.Column(db.String(255), nullable=False)

    def __init__(self, email, hash_, level):
        self.email = email
        self.hash = hash_
        self.level = level
