import yaml
from app import app, db
from flask import request
from app.database import Cafe, Menu, Photo
from app.helper import format_exception, to_bool


@app.route("/cafe/<cafe_id>", methods=["GET"], strict_slashes=False)
def get_cafe_info(cafe_id):
    try:
        cafe_id_int = int(cafe_id)

        cafe = Cafe.query.where(Cafe.id == cafe_id_int).first()
        menus = Menu.query.where(Menu.cafe_id == cafe_id_int).all()
        photos = Photo.query.where(Photo.cafe_id == cafe_id_int).all()

        menu_list = []
        photo_list = []

        for menu in menus:
            menu_list.append({
                "id": menu.id,
                "name": menu.name,
                "price": menu.price,
            })

        for photo in photos:
            photo_list.append({
                "id": photo.id,
                "photo_url": photo.photo_url,
            })

        if cafe != None:
            return {
                "msg": "success",
                "data": {
                    "id": cafe_id_int,
                    "name": cafe.name,
                    "logo_url": cafe.logo_url,
                    "rating_count": cafe.rating_count,
                    "rating_dec": float(cafe.rating_dec),
                    "menus": menu_list,
                    "photos": photo_list,
                    "contact": {
                        "whatsapp": cafe.whatsapp,
                        "instagram": cafe.instagram,
                        "gmaps": cafe.gmaps,
                        "website": cafe.website,
                        "address": cafe.address,
                    },
                },
            }
        else:
            return {
                "msg": "specified cafe not found",
            }, 422

    except BaseException as e:
        return {
            "msg": format_exception(e, __file__),
        }, 400


@app.route("/cafe/<cafe_id>/photos", methods=["GET"], strict_slashes=False)
def get_cafe_photos(cafe_id):
    try:
        cafe_id_int = int(cafe_id)
        args = request.args.to_dict()
        show_from_customer = args["show_from_customer"]
        limit = args["limit"]
        data = []

        if to_bool(show_from_customer):
            photos = Photo.query.where(Photo.id == cafe_id_int).limit(limit).all()
        else:
            photos = Photo.query.where((Photo.id == cafe_id_int) & (Photo.review_id != -1)).limit(limit).all()

        for photo in photos:
            data.append({
                "id": photo.id,
                "photo_url": photo.photo_url,
                "date": photo.date,
                "review_id": photo.review_id,
            })

        return {
            "msg": "success",
            "data": data,
        }
    except BaseException as e:
        return {
            "msg": format_exception(e, __file__),
        }, 400


@app.route("/cafes/search", methods=["GET"], strict_slashes=False)
def get_cafes_by_keyword():
    try:
        args = request.args.to_dict()
        keyword = args["keyword"]
        limit = args["limit"]
        data = []

        if int(limit) > 0:
            cafes = Cafe.query.filter(Cafe.name.ilike(f"%{keyword}%")).limit(limit).all()
        else:
            cafes = Cafe.query.filter(Cafe.name.ilike(f"%{keyword}%")).all()

        for cafe in cafes:
            photo = Photo.query.where(Photo.cafe_id == cafe.id).first()

            if (photo is not None):
                photo_dict = {
                    "id": photo.id,
                    "photo_url": photo.photo_url,
                }
            else:
                photo_dict = None

            data.append({
                "id": cafe.id,
                "name": cafe.name,
                "logo_url": cafe.logo_url,
                "photo": photo_dict,
                "rating_count": cafe.rating_count,
                "rating_dec": cafe.rating_dec,
            })

        return {
            "msg": "success",
            "data": data,
        }
    except BaseException as e:
        return {
            "msg": format_exception(e, __file__),
        }, 400


@app.route("/cafe/insert", methods=["POST"], strict_slashes=False)
def insert_cafe():
    try:
        req = yaml.safe_load(request.data)

        cafe = Cafe.query.where(Cafe.name == req["nama"]).first()

        if cafe is None:
            new_cafe = Cafe(
                name=req["nama"],
                logo_url="",
                whatsapp=req["whatsapp"],
                instagram=req["instagram"],
                gmaps=req["gmaps"],
                website=req["website"],
                address=req["alamat"],
            )

            db.session.add(new_cafe)
            db.session.commit()

            cafe_id = new_cafe.id
        else:
            cafe_id = cafe.id

        menus = Menu.query.where(Menu.cafe_id == cafe_id).all()
        photos = Photo.query.where(Photo.cafe_id == cafe_id).all()

        for menu in menus:
            db.session.delete(menu)
        for photo in photos:
            db.session.delete(photo)

        db.session.commit()

        for menu in req["menu"]:
            new_menu = Menu(
                cafe_id=cafe_id,
                name=menu["nama"],
                price=menu["harga"],
            )

            db.session.add(new_menu)

        for photo in req["foto"]:
            new_photo = Photo(
                cafe_id=cafe_id,
                photo_url=photo["url"],
            )

            db.session.add(new_photo)

        db.session.commit()

        return {
            "msg": "success",
        }
    except BaseException as e:
        return {
            "msg": format_exception(e, __file__),
        }, 400
