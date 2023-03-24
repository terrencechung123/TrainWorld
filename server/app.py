#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Restaurant, RestaurantPizza, Pizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)
api = Api(app)


class Restaurants(Resource):
    def get(self):
        restaurants = Restaurant.query.all()
        restaurants_dict_list = [restaurant.to_dict()
                                for restaurant in restaurants]
        response = make_response(
            restaurants_dict_list,
            200
        )
        return response

api.add_resource(Restaurants, '/restaurants')

class RestaurantById(Resource):
    def get(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if not restaurant:
            return make_response({
                "error": "Restaurant not found"
            }, 404)
        restaurant_dict = restaurant.to_dict(
            rules=('pizzas', ))
        response = make_response(restaurant_dict, 200)
        return response

    def delete(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()
        if not restaurant:
            return make_response({
                "error": "Restaurant not found"
            }, 404)

        db.session.delete(restaurant)
        db.session.commit()

api.add_resource(RestaurantById, '/restaurants/<int:id>')

class Pizzas(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        pizzas_dict_list = [pizza.to_dict()
                                for pizza in pizzas]
        response = make_response(
            pizzas_dict_list,
            200
        )

        return response
api.add_resource(Pizzas, '/pizzas')

class RestaurantPizzas(Resource):
    def post(self):
        data = request.get_json()
        try:
            restaurantpizza = RestaurantPizza(
                price=data['price'],
                pizza_id=data['pizza_id'],
                restaurant_id=data['restaurant_id']
            )
            db.session.add(restaurantpizza)
            db.session.commit()
        except Exception as e:
            return make_response({
                "errors": [e.__str__()]
            }, 422)
        response = make_response(
            restaurantpizza.to_dict(),
            201
        )
        return response
api.add_resource(RestaurantPizzas,'/restaurant_pizzas')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
