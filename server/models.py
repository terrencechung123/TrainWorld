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
    __tablename__ = 'users'

    serialize_rules = ('-recipes.user', '-_password_hash',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)

    recipes = db.relationship('Recipe', backref='user')

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


    # def __repr__(self):
    #     return f'<Recipe {self.id}: {self.title}>'