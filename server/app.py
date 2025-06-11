#!/usr/bin/env python3

from flask import request, session, make_response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from config import app, db, api, bcrypt
from models import db, User, Olive, Producer, OliveOil
from schemas import UserSchema, OliveSchema, ProducerSchema, OliveOilSchema

user_schema = UserSchema()
olive_schema = OliveSchema()
producer_schema = ProducerSchema()
oils_schema = OliveOilSchema()

@app.before_request
def check_if_logged_in():

    open_access_list = [
        'signup',
        'login',
        'check_session'
    ]

    if (request.endpoint) not in open_access_list and (not session.get('user_id')):

        result = make_response(
            {'error': '401 Unauthorized'},
            401
        )

        return result

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

    def post(self):

        fields = request.get_json()
        name = fields.get('name')
        country = fields.get('country')
        region = fields.get('region')
        color = fields.get('color')
        rarity = fields.get('rarity')

        new_olive = Olive(name=name, country=country, region=region, color=color, rarity=rarity)

        db.session.add(new_olive)
        db.session.commit()

        result = make_response(
            olive_schema.dump(new_olive),
            201
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

    def post(self):

        fields = request.get_json()
        name = fields.get('name')
        address = fields.get('address')
        capacity = fields.get('capacity')

        new_producer = Producer(name=name, address=address, capacity=capacity)

        db.session.add(new_producer)
        db.session.commit()

        result = make_response(
            producer_schema.dump(new_producer),
            201
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

    def post(self):

        fields = request.get_json()
        name = fields.get('name')
        year = fields.get('year')
        price = fields.get('price')
        acidity = fields.get('acidity')
        isActive = fields.get('isActive')
        producer_id = fields.get('producerId')
        olive_id = fields.get('oliveId')

        new_oil = OliveOil(
            name=name, 
            year=year, 
            price=price, 
            acidity=acidity, 
            isActive=isActive, 
            user_id=session['user_id'],
            producer_id=producer_id, 
            olive_id=olive_id
        )

        db.session.add(new_oil)
        db.session.commit()

        result = make_response(
            oils_schema.dump(new_oil),
            201
        )

        return result


class Oil(Resource):

    def patch(self, id):

        if not session.get('user_id'):

            result = make_response(
                {'error': '401 Unauthorized'},
                401
            )

            return result

        oil = OliveOil.query.get(id)

        if not oil:

            result = make_response(
                {'error': '404 Not Found'},
                404
            )

            return result

        if oil.user_id != session['user_id']:

            result = make_response(
                {'error': '403 Forbidden'},
                403
            )

            return result

        fields = request.get_json()
        name = fields.get('name')
        year = fields.get('year')
        price = fields.get('price')
        acidity = fields.get('acidity')
        isActive = fields.get('isActive')
        producer_id = fields.get('producerId')
        olive_id = fields.get('oliveId')


        if producer_id:
            producer = Producer.query.get(producer_id)

            if not producer:

                result = make_response(
                    {'error': '404 Not Found'},
                    404
                )

                return result
        
        if olive_id:
            olive = Olive.query.get(olive_id)

            if not olive:

                result = make_response(
                    {'error': '404 Not Found'},
                    404
                )

                return result

        try:
            if name is not None:
                oil.name = name

            if year is not None:
                oil.year = year

            if price is not None:
                oil.price = price

            if acidity is not None:
                oil.acidity = acidity

            if isActive is not None:
                oil.isActive = isActive

            if producer_id is not None:
                oil.producer_id = producer_id

            if olive_id is not None:
                oil.olive_id = olive_id

            db.session.commit()

            result = make_response(
                oils_schema.dump(oil),
                200
            )

            return result

        except IntegrityError:
            db.session.rollback()

            result = make_response(
                {'error': '422 Unprocessable Entity'},
                422
            )

            return result

        except ValueError as e:

            result = make_response(
                {'error': str(e)},
                422
            )

            return result

    def delete(self, id):

        if not session.get('user_id'):

            result = make_response(
                {'error': '401 Unauthorized'},
                401
            )

            return result

        oil = OliveOil.query.get(id)

        if not oil:

            result = make_response(
                {'error': '404 Not Found'},
                404
            )

            return result

        if oil.user_id != session['user_id']:

            result = make_response(
                {'error': '403 Forbidden'},
                403
            )

            return result

        try:
            db.session.delete(oil)
            db.session.commit()

            result = make_response(
                {'message': '204: No Content'},
                204
            )

            return result

        except Exception as e:
            db.session.rollback()

            result = make_response(
                {'error': str(e)},
                422
            )

            return result

class Signup(Resource):

    def post(self):

        fields = request.get_json()
        username = fields.get('username')
        password = fields.get('password')

        if not username or not password:

            result = make_response(
                {'error': 'Username and password required'},
                422
            )

            return result

        try:
            new_user = User(username=username)
            new_user.password = password

            db.session.add(new_user)
            db.session.commit()

            session['user_id'] = new_user.id

            result = make_response(
                user_schema.dump(new_user),
                201
            )

            return result

        except IntegrityError:
            db.session.rollback()

            result = make_response(
                {'error': '422 Unprocessable Entity - Username taken'},
                422
            )

            return result

        except ValueError as e:

            result = make_response(
                {'error': str(e)},
                422
            )

            return result

class CheckSession(Resource):

    def get(self):

        try:
            user_id = session.get('user_id')

            if not user_id:
                return make_response({}, 401)

            user = User.query.get(user_id)

            if not user:
                return make_response({}, 401)
            
            producer_map ={}

            for oil in user.oils:
                producer = oil.producer

                if producer and producer.id not in producer_map:
                    producer_map[producer.id] = {
                        "id": producer.id,
                        "name": producer.name,
                        "address": producer.address,
                        "capacity": producer.capacity,
                        "olives": []
                    }
                
                producer_map[producer.id]["olives"].append(oils_schema.dump(oil))

            user_schema = UserSchema()
            user_data = user_schema.dump(user)

            result = make_response(
                user_data,
                200
            )

            return result

        except Exception as e:
            print("CheckSession error:", e)

            result = make_response(
                {'error': 'Server error during session check'},
                500
            )

            return result

class Login(Resource):

    def post(self):
    
        try:
            request_json = request.get_json()
            username = request_json.get('username')
            password = request_json.get('password')

            print("Username:", username)
            print("Password:", password)

            user = User.query.filter_by(username=username).one_or_none()
            print("User found:", user)

            if user and user.authenticate(password):
                session['user_id'] = user.id

                result = make_response(
                    user_schema.dump(user),
                    200
                )

            else:

                result = make_response(
                    {'error': '401 Unauthorized'}, 
                    401
                )

            return result

        except Exception as e:
            print("Login error:", e)

            result = make_response(
                {'error': 'Server error during login'},
                500
            )

            return result

class Logout(Resource):

    def delete(self):

        session['user_id'] = None

        result = make_response(
            {'message': '204: No Content'},
            204
        )

        return result

api.add_resource(Users, '/users', endpoint='users')
api.add_resource(Olives, '/olives', endpoint='olives')
api.add_resource(Producers, '/producers', endpoint='producers')
api.add_resource(Oils, '/oils', endpoint='oils')
api.add_resource(Oil, '/oils/<int:id>', endpoint='oil')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
