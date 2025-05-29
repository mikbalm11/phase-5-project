#!/usr/bin/env python3

from flask import request, session, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from config import app, db, api, bcrypt
from models import User, Olive, Producer, OliveOil

class Users(Resource):

    def get(self):

        users = User.query.all()

        result = make_response(
            [user.to_dict() for user in users],
            200
        )

        return result

class Olives(Resource):

    def get(self):

        olives = Olive.query.all()

        result = make_response(
            [olive.to_dict() for olive in olives],
            200
        )

        return result

class Producers(Resource):

    def get(self):

        producers = Producer.query.all()

        result = make_response(
            [producer.to_dict() for producer in producers],
            200
        )

        return result

class Oils(Resource):

    def get(self):

        oils = OliveOil.query.all()

        result = make_response(
            [oil.to_dict() for oil in oils],
            200
        )

        return result

api.add_resource(Users, '/users', endpoint='users')
api.add_resource(Olives, '/olives', endpoint='olives')
api.add_resource(Producers, '/producers', endpoint='producers')
api.add_resource(Oils, '/oils', endpoint='oils')

if __name__ == '__main__':
    app.run(port=5555, debug=True)

