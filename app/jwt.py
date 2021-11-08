from app import jwt
from app.database import User


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.email


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]

    return User.query.filter_by(email=identity).one_or_none()


@jwt.invalid_token_loader
def invalid_token_callback(_jwt_data):
    return {
        "msg": "invalid token"
    }, 401


@jwt.expired_token_loader
def expired_token_callback(_jwt_header, jwt_data):
    return {
        "msg": "token expired"
    }, 401
