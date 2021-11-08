import sqlalchemy
from app import app, db, jwt
from app.database import User
from flask import request
from flask_jwt_extended import jwt_required, current_user, create_access_token


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.email


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(email=identity).one_or_none()


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
                "msg": "username is already exists",
            }, 400
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
                "email": user.email,
                "level": user.level,
                "access_token": create_access_token(identity=user),
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
