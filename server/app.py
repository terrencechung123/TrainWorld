#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request, session
from flask_migrate import Migrate
from flask_restful import Api, Resource
from sqlalchemy.exc import IntegrityError

from models import db, Conductor, TrainRide, Train
from config import app, db, api

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

api.add_resource(Conductors, '/conductors')

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

api.add_resource(ConductorById, '/conductors/<int:id>')

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
api.add_resource(Trains, '/trains')

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
api.add_resource(TrainRides,'/train_rides')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
