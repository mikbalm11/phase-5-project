from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field, fields
from config import ma
from models import User, Olive, Producer, OliveOil

class UserSchema(SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True

    id = auto_field()
    username = auto_field()

    oils = fields.Nested('OliveOilSchema', many=True, exclude=('user',))

class OliveSchema(SQLAlchemySchema):
    class Meta:
        model = Olive
        load_instance = True

    id = auto_field()
    name = auto_field()
    country = auto_field()
    region = auto_field()
    color = auto_field()
    rarity = auto_field()

    oils = fields.Nested('OliveOilSchema', many=True, exclude=('olive', 'producer', 'user'))

class ProducerSchema(SQLAlchemySchema):
    class Meta:
        model = Producer
        load_instance = True

    id = auto_field()
    name = auto_field()
    address = auto_field()
    capacity = auto_field()

    oils = fields.Nested('OliveOilSchema', many=True, exclude=('producer', 'olive', 'user'))

class OliveOilSchema(SQLAlchemySchema):
    class Meta:
        model = OliveOil
        load_instance = True

    id = auto_field()
    name = auto_field()
    year = auto_field()
    price = auto_field()
    isActive = auto_field()
    acidity = auto_field()

    # user_id = auto_field()
    # producer_id = auto_field()
    # olive_id = auto_field()

    user = fields.Nested(UserSchema, only=("id", "username"))
    olive = fields.Nested(OliveSchema, exclude=("oils",))
    producer = fields.Nested(ProducerSchema, exclude=("oils",))
