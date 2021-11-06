from app import db


class Cafe(db.Model):
    id_ = db.Column(db.String(8), primary_key=True)
