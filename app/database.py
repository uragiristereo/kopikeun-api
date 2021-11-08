from app import db


class User(db.Model):
    email = db.Column(db.String(64), primary_key=True)
    hash = db.Column(db.String(64), unique=True, nullable=False)
    level = db.Column(db.String(8), nullable=False)

    def __init__(self, email, hash, level):
        self.email = email
        self.hash = hash
        self.level = level


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    cafe_id = db.Column(db.Integer, db.ForeignKey("cafe.id"), nullable=False)
