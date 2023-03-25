from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-trains.user', '-_password_hash',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)

    trains = db.relationship('Train', backref='user')


    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password hashes may not be viewed.')

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))

    def __repr__(self):
        return f'<User {self.username}>'

class Train(db.Model, SerializerMixin):
    __tablename__ = 'trains'
    # __table_args__ = (
    #     db.CheckConstraint('length(description) >= 50'),
    # )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    # minutes_to_complete = db.Column(db.Integer)
    avatar = db.Column(db.String)


    reviews = db.relationship('Review', backref='train')
    locations = association_proxy('reviews', 'location')
    users = association_proxy('reviews', 'user')

    def __repr__(self):
        return f'<Train {self.id}: {self.title}>'

class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    train_id = db.Column(db.Integer, db.ForeignKey('trains.id'))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    title = db.Column(db.String)
    description = db.Column(db.String)
    rating = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, server_default=db.func.now())

class Location(db.Model, SerializerMixin):
    __tablename__ = 'locations'

    serialize_rules = ('-reviews','-created_at','-location_id','-updated_at')
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    avatar = db.Column(db.String)
    address = db.Column(db.String)

    reviews = db.relationship('Review', backref='location')
    trains = association_proxy('reviews', 'train')
    users = association_proxy('reviews', 'user')

# class Train(db.Model, SerializerMixin):
#     __tablename__ = 'trains'

#     serialize_rules = ('-reviews','-created_at','-updated_at','-reviews')
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String)
#     description = db.Column(db.String)
#     avatar = db.Column(db.String)

#     reviews = db.relationship('Review', backref='train')
#     locations = association_proxy('reviews', 'location')
#     users = association_proxy('reviews', 'user')