#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request, session
from flask_migrate import Migrate
from flask_restful import Api, Resource
from sqlalchemy.exc import IntegrityError

from models import db, Conductor, TrainRide, Train
from config import app, db, api

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

class Conductors(Resource):
    def get(self):
        conductors = Conductor.query.all()
        conductors_dict_list = [conductor.to_dict()
                                for conductor in conductors]
        response = make_response(
            conductors_dict_list,
            200
        )
        return response


class ConductorById(Resource):
    def get(self, id):
        conductor = Conductor.query.filter_by(id=id).first()
        if not conductor:
            return make_response({
                "error": "Conductor not found"
            }, 404)
        conductor_dict = conductor.to_dict(
            rules=('trains', ))
        response = make_response(conductor_dict, 200)
        return response

    def delete(self, id):
        conductor = Conductor.query.filter_by(id=id).first()
        if not conductor:
            return make_response({
                "error": "Conductor not found"
            }, 404)

        db.session.delete(conductor)
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

class TrainRides(Resource):
    def post(self):
        data = request.get_json()
        try:
            trainRide = TrainRide(
                train_id=data['train_id'],
                conductor_id=data['conductor_id']
            )
            db.session.add(trainRide)
            db.session.commit()
        except Exception as e:
            return make_response({
                "errors": [e.__str__()]
            }, 422)
        response = make_response(
            trainRide.to_dict(),
            201
        )
        return response


api.add_resource(ConductorById, '/conductors/<int:id>')
api.add_resource(Trains, '/trains')
api.add_resource(TrainRides,'/train_rides')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(Conductors, '/conductors')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
