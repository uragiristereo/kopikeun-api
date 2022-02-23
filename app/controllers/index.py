from app import app, db
from os import environ


@app.route("/", methods=["GET"])
def index():
    return "Kopikeun"


@app.route("/reset", methods=["GET"])
def reset():
    database_url = environ.get("DATABASE_URL")

    # if database_url == None:
    db.drop_all()
    db.create_all()

    return {
        "msg": "the database has been successfully reset"
    }
    # else:
    #     return {
    #         "msg": "you're not allowed to do this operation"
    #     }, 403
