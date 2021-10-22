from app import app
from app.models.user import User


@app.route('/login', methods=['GET'])
def login():
    user = User()
    return "login {}".format(user.getNama())
