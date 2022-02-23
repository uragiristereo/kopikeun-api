from app import app, db
from flask import request
from app.database import Photo, Review
from app.helper import format_exception


@app.route("/cafe/<cafe_id>/reviews", methods=["GET"], strict_slashes=False)
def get_cafe_reviews(cafe_id):
    try:
        args = request.args.to_dict()
        data = []

        reviews = Review.query.where(Review.cafe_id == int(cafe_id)).limit(args["limit"]).all()

        for review in reviews:
            data.append({
                "id": review.id,
                "user_email": review.user_email,
                "rating": review.rating,
                "content": review.content,
                "date": review.date,
            })

        return {
            "msg": "success",
            "data": data,
        }
    except BaseException as e:
        return {
            "msg": format_exception(e, __file__),
        }, 400


@app.route("/cafe/<cafe_id>/review/<review_id>", methods=["GET"], strict_slashes=False)
def get_cafe_review(cafe_id, review_id):
    try:
        cafe_id_int = int(cafe_id)
        review_id_int = int(review_id)
        photos = []

        review = Review.query.where((Review.id == review_id_int) & (Review.cafe_id == cafe_id_int)).first()
        review_photos = Photo.query.where(Photo.review_id == review_id_int).all()

        for review_photo in review_photos:
            photos.append({
                "id": review_photo.id,
                "photo_url": review_photo.photo_url,
                "date": review_photo.date.isoformat(),
            })

        return {
            "msg": "success",
            "data": {
                "id": review.id,
                "user_email": review.user_email,
                "cafe_id": review.cafe_id,
                "rating": review.rating,
                "content": review.content,
                "date": review.date.isoformat(),
                "cafe": {
                    "name": review.cafe.name,
                    "logo_url": review.cafe.logo_url,
                    "rating_count": review.cafe.rating_count,
                    "rating_dec": review.cafe.rating_dec,
                },
                "photos": photos,
            }
        }
    except BaseException as e:
        return {
            "msg": format_exception(e, __file__),
        }, 400


@app.route("/cafe/<cafe_id>/review/add", methods=["POST"], strict_slashes=False)
def add_cafe_review(cafe_id):
    try:
        req = request.get_json()

        review = Review(
            user_email=req["user_email"],
            cafe_id=int(cafe_id),
            rating=req["rating"],
            content=req["content"],
        )

        try:
            db.session.add(review)
            db.session.commit()
            db.session.flush()

            return {
                "msg": "success",
                "data": {
                    "review_id": review.id,
                }
            }
        except:
            return {
                "msg": "can't add review",
            }, 422
    except BaseException as e:
        return {
            "msg": format_exception(e, __file__),
        }, 400
