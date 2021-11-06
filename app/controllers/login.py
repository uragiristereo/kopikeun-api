from app import app, db


@app.route("/register", methods=["POST"])
def login():
    return "register"
