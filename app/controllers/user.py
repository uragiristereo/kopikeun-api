from app import app, db, jwt
from app.database import User
from flask import request
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, current_user, create_access_token, get_jwt_identity, create_refresh_token
from hashlib import sha256
from os import environ


@app.route("/user/register", methods=["POST"], strict_slashes=False)
def register():
    req = request.get_json()

    if type(req) == dict:
        jwt_secret_key = environ.get("JWT_SECRET_KEY")
        hash = sha256(jwt_secret_key.encode() + req["email"].encode()).hexdigest()

        if req["hash"] != hash:
            return {
                "msg": "email and hash is not match",
            }, 422

        user = User(req["email"], req["hash"], req["level"])

        try:
            db.session.add(user)
            db.session.commit()

            return {
                "email": user.email,
                "level": user.level,
            }
        except IntegrityError as e:
            return {
                "msg": "user is already exists",
            }, 422
    else:
        return {
            "msg": "invalid request input",
        }, 400


@app.route("/user/login", methods=["POST"], strict_slashes=False)
def login():
    req = request.get_json()

    if type(req) == dict:
        user = User.query.where((User.email == req["email"]) & (User.hash == req["hash"])).first()

        if user != None:
            return {
                "access_token": create_access_token(identity=user),
                "refresh_token": create_refresh_token(identity=user),
            }
        else:
            return {
                "msg": "invalid email or hash",
            }, 401
    else:
        return {
            "msg": "invalid request input",
        }, 400


@app.route("/user/info", methods=["POST"], strict_slashes=False)
@jwt_required()
def userInfo():
    return {
        "email": current_user.email,
        "level": current_user.level,
    }


@app.route("/user/refresh_token", methods=["POST"], strict_slashes=False)
@jwt_required(refresh=True)
def refreshToken():
    identity = get_jwt_identity()
    user = User.query.where(User.email == identity).first()
    access_token = create_access_token(identity=user)

    return {
        "access_token": access_token,
    }
