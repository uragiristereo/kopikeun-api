from werkzeug.datastructures import MultiDict
from app import app, db
from app.database import Favorite, User
from flask import request
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, current_user, create_access_token, get_jwt_identity, create_refresh_token
from hashlib import sha256
from os import environ

from app.helper import format_exception


@app.route("/user/register", methods=["POST"], strict_slashes=False)
def register():
    try:
        form = request.form.to_dict()
        email = form["email"]
        hash_str = form["hash"]
        jwt_secret_key = environ.get("JWT_SECRET_KEY")
        hash = sha256(jwt_secret_key.encode() + email.encode()).hexdigest()

        if hash_str != hash:
            return {
                "msg": "email and hash is not match",
                "data": None,
            }, 422

        user = User(
            email=email,
            hash=hash_str,
            level="customer",
        )

        try:
            db.session.add(user)
            db.session.commit()

            return {
                "msg": "success",
                "data": {
                    "email": user.email,
                    "level": user.level,
                },
            }
        except IntegrityError:
            return {
                "msg": "user is already exists",
            }, 422
    except BaseException as e:
        return {
            "msg": format_exception(e, __file__),
        }, 400


@app.route("/user/login", methods=["POST"], strict_slashes=False)
def login():
    try:
        form = request.form.to_dict()
        email = form["email"]
        hash_str = form["hash"]

        print(type(User.email))

        user = User.query.where((User.email == email) & (User.hash == hash_str)).first()

        if user != None:
            return {
                "msg": "success",
                "data": {
                    "access_token": create_access_token(identity=user),
                    "refresh_token": create_refresh_token(identity=user),
                },
            }
        else:
            return {
                "msg": "invalid email or hash",
            }, 401
    except BaseException as e:
        return {
            "msg": format_exception(e, __file__),
        }, 400


@app.route("/user/info", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_user_info():
    return {
        "msg": "success",
        "data": {
            "email": current_user.email,
            "level": current_user.level,
        },
    }


@app.route("/user/refresh_token", methods=["GET"], strict_slashes=False)
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    user = User.query.where(User.email == identity).first()
    access_token = create_access_token(identity=user)

    return {
        "msg": "success",
        "data": {
            "access_token": access_token,
        },
    }


@app.route("/user/favorites", methods=["GET"], strict_slashes=False)
@jwt_required()
def get_favorites():
    identity = get_jwt_identity()
    favorites = Favorite.query.where(Favorite.user_email == identity).all()
    data = []

    for favorite in favorites:
        data.append({
            "id": favorite.id,
            "cafe_id": favorite.cafe_id,
        })

    return {
        "msg": "success",
        "data": data,
    }
