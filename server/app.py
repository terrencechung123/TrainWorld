#!/usr/bin/env python3

from flask import request, session
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from config import app, db, api
from models import db, User, Train

class Signup(Resource):

    def post(self):
        request_json = request.get_json()
        username = request_json.get('username')
        password = request_json.get('password')
        image_url = request_json.get('image_url')
        bio = request_json.get('bio')
        user = User(
            username=username,
            image_url=image_url,
            bio=bio
        )

        # the setter will encrypt this
        user.password_hash = password
        print('first')
        try:
            print('here!')
            db.session.add(user)
            db.session.commit()
            session['user_id'] = user.id
            print(user.to_dict())
            return user.to_dict(), 201
        except IntegrityError:
            print('no, here!')
            return {'error': '422 Unprocessable Entity'}, 422

class CheckSession(Resource):
    def get(self):
        if session.get('user_id'):
            user = User.query.filter(User.id == session['user_id']).first()
            return user.to_dict(), 200
        return {'error': '401 Unauthorized'}, 401

class Login(Resource):
    def post(self):
        request_json = request.get_json()
        username = request_json.get('username')
        password = request_json.get('password')
        user = User.query.filter(User.username == username).first()
        if user:
            if user.authenticate(password):
                session['user_id'] = user.id
                return user.to_dict(), 200
        return {'error': '401 Unauthorized'}, 401

class Logout(Resource):

    def delete(self):
        if session.get('user_id'):
            session['user_id'] = None
            return {}, 204
        return {'error': '401 Unauthorized'}, 401

class TrainIndex(Resource):
    def get(self):
        if session.get('user_id'):
            user = User.query.filter(User.id == session['user_id']).first()
            return [train.to_dict() for train in user.trains], 200
        return {'error': '401 Unauthorized'}, 401
    def post(self):
        if session.get('user_id'):
            request_json = request.get_json()
            title = request_json['title']
            description = request_json['description']
            # minutes_to_complete = request_json['minutes_to_complete']
            try:
                train = Train(
                    title=title,
                    description=description,
                    # minutes_to_complete=minutes_to_complete,
                    user_id=session['user_id'],
                )
                db.session.add(train)
                db.session.commit()
                return train.to_dict(), 201
            except IntegrityError:
                return {'error': '422 Unprocessable Entity'}, 422
        return {'error': '401 Unauthorized'}, 401


class Locations(Resource):
    def get(self):
        locations = Location.query.all()
        locations_dict_list = [location.to_dict()
                                for location in locations]
        response = make_response(
            locations_dict_list,
            200
        )
        return response


class LocationById(Resource):
    def get(self, id):
        location = Location.query.filter_by(id=id).first()
        if not location:
            return make_response({
                "error": "Location not found"
            }, 404)
        location_dict = location.to_dict(
            rules=('trains', ))
        response = make_response(location_dict, 200)
        return response

    def delete(self, id):
        location = Location.query.filter_by(id=id).first()
        if not location:
            return make_response({
                "error": "Location not found"
            }, 404)

        db.session.delete(location)
        db.session.commit()


class Trains(Resource):
    def get(self):
        trains = Train.query.all()
        trains_dict_list = [train.to_dict()
                                for train in trains]
        response = make_response(
            trains_dict_list,
            200
        )

        return response


class Reviews(Resource):
    def post(self):
        data = request.get_json()
        try:
            review = Review(
                train_id=data['train_id'],
                location_id=data['location_id']
            )
            db.session.add(review)
            db.session.commit()
        except Exception as e:
            return make_response({
                "errors": [e.__str__()]
            }, 422)
        response = make_response(
            review.to_dict(),
            201
        )
        return response


api.add_resource(Locations, '/locations')
api.add_resource(LocationById, '/locations/<int:id>')
api.add_resource(Reviews,'/train_rides')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(TrainIndex, '/train_index', endpoint='train_index')
api.add_resource(Trains, '/trains')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
