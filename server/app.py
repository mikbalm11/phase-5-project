#!/usr/bin/env python3

from flask import request, session, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from config import app, db, api, bcrypt
from models import db, User, Olive, Producer, OliveOil
from schemas import UserSchema, OliveSchema, ProducerSchema, OliveOilSchema

class Users(Resource):

    def get(self):

        users = User.query.all()

        result = make_response(
            UserSchema(many=True).dump(users),
            200
        )

        return result

class Olives(Resource):

    def get(self):

        olives = Olive.query.all()

        result = make_response(
            OliveSchema(many=True).dump(olives),
            200
        )

        return result

class Producers(Resource):

    def get(self):

        producers = Producer.query.all()

        result = make_response(
            ProducerSchema(many=True).dump(producers),
            200
        )

        return result

class Oils(Resource):

    def get(self):

        oils = OliveOil.query.all()

        result = make_response(
            OliveOilSchema(many=True).dump(oils),
            200
        )

        return result

api.add_resource(Users, '/users', endpoint='users')
api.add_resource(Olives, '/olives', endpoint='olives')
api.add_resource(Producers, '/producers', endpoint='producers')
api.add_resource(Oils, '/oils', endpoint='oils')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

