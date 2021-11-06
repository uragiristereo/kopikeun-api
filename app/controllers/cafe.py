from app import app
from flask import jsonify


@app.route("/cafe/<cafe_id>", methods=["GET"], strict_slashes=False)
def getCafeData(cafe_id):
    # return cafe_id
    return jsonify({
        "id": cafe_id,
        "name": "Kopi anu",
        "icon": "https://",
        "contact": {
            "whatsapp": "",
            "instagram": "",
            "gmaps": "",
            "website": "",
            "alamat": "",
        }
    })


@app.route("/cafe/<cafe_id>/photos", methods=["GET"], strict_slashes=False)
def getCafePhotos(cafe_id):
    return cafe_id


@app.route("/cafe/<cafe_id>/reviews", methods=["GET"], strict_slashes=False)
def getCafeReviews(cafe_id):
    return cafe_id


@app.route("/cafe/<cafe_id>/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def getCafeReview(cafe_id, review_id):
    return cafe_id
