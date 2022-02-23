from app import db


class Cafe(db.Model):
    __tablename__ = 'cafe'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    name = db.Column(db.String(64), nullable=False)
    logo_url = db.Column(db.String(255), nullable=False)
    whatsapp = db.Column(db.String(16))
    instagram = db.Column(db.String(255))
    gmaps = db.Column(db.String(255))
    website = db.Column(db.String(255))
    address = db.Column(db.String(255))
    rating_count = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())
    rating_dec = db.Column(db.Numeric, nullable=False, server_default=db.FetchedValue())

    def to_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class Favorite(db.Model):
    __tablename__ = 'favorite'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    user_email = db.Column(db.ForeignKey('user.email', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    cafe_id = db.Column(db.ForeignKey('cafe.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)

    cafe = db.relationship('Cafe', primaryjoin='Favorite.cafe_id == Cafe.id', backref='favorites')
    user = db.relationship('User', primaryjoin='Favorite.user_email == User.email', backref='favorites')


class Menu(db.Model):
    __tablename__ = 'menu'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    cafe_id = db.Column(db.ForeignKey('cafe.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    cafe = db.relationship('Cafe', primaryjoin='Menu.cafe_id == Cafe.id', backref='menus')


class Photo(db.Model):
    __tablename__ = 'photo'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    cafe_id = db.Column(db.ForeignKey('cafe.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    photo_url = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    review_id = db.Column(db.Integer, nullable=False, server_default=db.FetchedValue())

    cafe = db.relationship('Cafe', primaryjoin='Photo.cafe_id == Cafe.id', backref='photos')
    reviews = db.relationship('Review', secondary='review_linked', backref='photos')


class Review(db.Model):
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True, server_default=db.FetchedValue())
    user_email = db.Column(db.ForeignKey('user.email', ondelete='SET DEFAULT', onupdate='CASCADE'), nullable=False, server_default=db.FetchedValue())
    cafe_id = db.Column(db.ForeignKey('cafe.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())

    cafe = db.relationship('Cafe', primaryjoin='Review.cafe_id == Cafe.id', backref='reviews')
    user = db.relationship('User', primaryjoin='Review.user_email == User.email', backref='reviews')


t_review_linked = db.Table(
    'review_linked',
    db.Column('photo_id', db.ForeignKey('photo.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False),
    db.Column('review_id', db.ForeignKey('review.id', ondelete='SET DEFAULT', onupdate='CASCADE'), nullable=False, server_default=db.FetchedValue())
)


class Update(db.Model):
    __tablename__ = 'update'

    version_code = db.Column(db.Integer, primary_key=True)
    version_name = db.Column(db.String(16), nullable=False)
    update_required = db.Column(db.Boolean, nullable=False, server_default=db.FetchedValue())


class User(db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String(64), primary_key=True)
    hash = db.Column(db.String(64), nullable=False, unique=True)
    level = db.Column(db.String(8), nullable=False)
