#!/usr/bin/env python3
from flask import Flask, request, make_response, jsonify
from flask_restful import Api, Resource
from flask_migrate import Migrate
from models import db, Restaurant, Pizza, RestaurantPizza
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)
api = Api(app)


@app.route("/")
def index():
    return "<h1>Code Challenge: Pizza Restaurant</h1>"


# GET
@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return make_response(jsonify([{
        "id": restaurant.id,
        "name": restaurant.name,
        "address": restaurant.address
    } for restaurant in restaurants]), 200)


# GET
@app.route("/restaurants/<int:id>", methods=["GET"])
def get_restaurant_by_id(id):
    restaurant = db.session.get(Restaurant, id)
    if restaurant:
        return make_response(jsonify(restaurant.to_dict()), 200)
    return make_response({"error": "Restaurant not found"}, 404)


# DELETE
@app.route("/restaurants/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    restaurant = db.session.get(Restaurant, id)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return make_response({}, 204)
    return make_response({"error": "Restaurant not found"}, 404)


# GET
@app.route("/pizzas", methods=["GET"])
def get_pizzas():
    pizzas = Pizza.query.all()
    return make_response(jsonify([pizza.to_dict() for pizza in pizzas]), 200)


# POST
@app.route("/restaurant_pizzas", methods=["POST"])
def create_restaurant_pizza():
    data = request.get_json()
    try:
        new_rp = RestaurantPizza(
            price=data["price"],
            restaurant_id=data["restaurant_id"],
            pizza_id=data["pizza_id"]
        )
        db.session.add(new_rp)
        db.session.commit()
        return make_response(jsonify(new_rp.to_dict()), 201)
    except ValueError as e:
        return make_response({"errors": ["validation errors"]}, 400)
    except KeyError as e:
        return make_response({"errors": ["validation errors"]}, 400)



if __name__ == "__main__":
    app.run(port=5555, debug=True)
