from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class TrainRide(db.Model, SerializerMixin):
    __tablename__ = 'train_rides'

    serialize_rules = ('-train', '-conductor',)

    id = db.Column(db.Integer, primary_key=True)
    train_id = db.Column(db.Integer, db.ForeignKey('conductors.id'))
    conductor_id = db.Column(db.Integer, db.ForeignKey('trains.id'))
    start_time = db.Column(db.DateTime, server_default = db.func.now())
    end_time = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())


class Conductor(db.Model, SerializerMixin):
    __tablename__ = 'conductors'

    serialize_rules = ('-train_rides','-created_at','-conductor_id','-updated_at')
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    avatar = db.Column(db.String)

    train_rides = db.relationship('TrainRide', backref='conductor')
    trains = association_proxy('train_rides', 'train')




class Train(db.Model, SerializerMixin):
    __tablename__ = 'trains'

    serialize_rules = ('-train_rides','-created_at','-updated_at','-train_rides')
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    avatar = db.Column(db.String)

    train_rides = db.relationship('TrainRide', backref='train')
    conductors = association_proxy('train_rides', 'conductor')

class User(db.Model, SerializerMixin):
    __table__ = 'users'

    pass