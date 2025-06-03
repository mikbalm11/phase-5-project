from config import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    _password = db.Column(db.String, nullable=False)

    oils = db.relationship('OliveOil', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User id={self.id} username={self.username}>'

class Olive(db.Model):
    __tablename__ = "olives"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    country = db.Column(db.String, nullable=False)
    region = db.Column(db.String, nullable=False)
    color = db.Column(db.String, nullable=False)
    rarity = db.Column(db.String, nullable=False)

    oils = db.relationship('OliveOil', back_populates='olive', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Olive id={self.id} name={self.name}>'

class Producer(db.Model):
    __tablename__ = "producers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    address = db.Column(db.String, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    oils = db.relationship('OliveOil', back_populates='producer', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Producer id={self.id} name={self.name}>'

class OliveOil(db.Model):
    __tablename__ = "oils"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    isActive = db.Column(db.Boolean, nullable=False)
    acidity = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    producer_id = db.Column(db.Integer, db.ForeignKey('producers.id'), nullable=False)
    olive_id = db.Column(db.Integer, db.ForeignKey('olives.id'), nullable=False)

    user = db.relationship('User', back_populates='oils')
    olive = db.relationship('Olive', back_populates='oils')
    producer = db.relationship('Producer', back_populates='oils')

    def __repr__(self):
        return f'<OliveOil id={self.id} name={self.name}>'
