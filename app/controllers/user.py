import sqlalchemy
from app import app, db
from app.database import User
from flask import request


@app.route("/user/register", methods=["POST"], strict_slashes=False)
def register():
    req = request.get_json()

    if type(req) == dict:
        user = User(req["email"], req["hash"], req["level"])

        try:
            db.session.add(user)
            db.session.commit()

            return {
                "email": user.email,
                "level": user.level,
            }
        except sqlalchemy.exc.IntegrityError as e:
            return {
                "message": "username is already exists",
            }, 400
    else:
        return {
            "message": "invalid request input",
        }, 400


@app.route("/user/login", methods=["POST"], strict_slashes=False)
def login():
    req = request.get_json()

    if type(req) == dict:
        user = User.query.where((User.email == req["email"]) & (User.hash == req["hash"])).first()

        if user != None:
            return {
                "email": user.email,
                "level": user.level,
            }
        else:
            return {
                "message": "invalid email or hash",
            }, 401
    else:
        return {
            "message": "invalid request input",
        }, 400
