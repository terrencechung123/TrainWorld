#!/usr/bin/env python3

from flask import request, session, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_login import current_user

from config import app, db, api
from models import db, User, Ticket, Train

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

class TicketIndex(Resource):
    def get(self):
        if session.get('user_id'):
            user = User.query.filter(User.id == session['user_id']).first()
            return [ticket.to_dict() for ticket in user.tickets], 200
        return {'error': '401 Unauthorized'}, 401
    def post(self):
        if session.get('user_id'):
            request_json = request.get_json()
            price = request_json['price']
            description = request_json['description']
            # minutes_to_complete = request_json['minutes_to_complete']
            try:
                ticket = Ticket(
                    price=price,
                    description=description,
                    # minutes_to_complete=minutes_to_complete,
                    user_id=session['user_id'],
                )
                db.session.add(ticket)
                db.session.commit()
                return ticket.to_dict(), 201
            except IntegrityError:
                return {'error': '422 Unprocessable Entity'}, 422
        return {'error': '401 Unauthorized'}, 401



class TicketById(Resource):
    def get(self, id):
        ticket = Ticket.query.filter_by(id=id).first()
        if not ticket:
            return make_response({
                "error": "Ticket not found"
            }, 404)
        ticket_dict = ticket.to_dict(
            rules=('train',))
        response = make_response(ticket_dict, 200)
        return response

    # def patch(self, id):
    #     ticket = Ticket.query.filter_by(id=id).first()

    #     data = request.get_json()
    #     for attr in data:
    #             setattr(ticket, attr, data[attr])

    #             db.session.add(ticket)
    #             db.session.commit()

    #             return make_response(
    #                 ticket.to_dict(),
    #                 202
    #             )
    def patch(self, id):
        ticket = Ticket.query.filter_by(id=id).first()

        if not ticket:
            return make_response({
                "error": "Ticket not found"
            }, 404)

        data = request.get_json()
        for attr in data:
            setattr(ticket, attr, data[attr])

        db.session.add(ticket)
        db.session.commit()

        return make_response(
            ticket.to_dict(),
            202
        )

    def delete(self, id):
        # user_id = get_current_user_id()
        # ticket = Ticket.query.filter_by(id=id, user_id=user_id).first()
        ticket = Ticket.query.filter_by(id=id).first()
        if not ticket:
            return make_response({
                "error": "Ticket not found"
            }, 404)

        db.session.delete(ticket)
        db.session.commit()
        return make_response({}, 204)
    
api.add_resource(TicketById, '/tickets/<int:id>')



class Tickets(Resource):
    def get(self):
        tickets = Ticket.query.all()
        tickets_dict_list = [ticket.to_dict()
                                for ticket in tickets]
        response = make_response(
            tickets_dict_list,
            200
        )
        return response

    def post(self):
        data =request.get_json()
        ticket = Ticket(
            price = data['price'],
            # train - data["train"],
            train_id = data['train_id'],
            #user = data["user"],
            user_id = data["user_id"]
        )
        db.session.add(ticket)
        db.session.commit()
        return make_response(ticket.to_dict(),201)

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


    def post(self):
        data = request.get_json()
        try:
            train = Train(
                title = data["title"],
                description = data["description"],
                image_url = data["image_url"]
            )
            db.session.add(train)
            db.session.commit()

        except Exception as e:
            return make_response({
               "errors": [e.__str__()]
           }, 422)


        return make_response(
            train.to_dict(),
            201
        )

class TrainById(Resource):
    def get(self, id):
        train = Train.query.filter_by(id=id).first().to_dict()
        return make_response(
            train,
            200)
api.add_resource(TrainById, "/trains/<int:id>")



class Users(Resource):
    def get(self):
        users = User.query.all()
        users_dict_list = [user.to_dict()
                                for user in users]
        response = make_response(
            users_dict_list,
            200
        )

        return response

class UserById(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first().to_dict()
        return make_response(
            user,
            200)
api.add_resource(UserById, "/users/<int:id>")

api.add_resource(Users,'/users')
api.add_resource(Trains, '/trains')
api.add_resource(Tickets, '/tickets')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(TicketIndex, '/ticket_index', endpoint='ticket_index')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
