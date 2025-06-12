from config import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
import re

OLIVE_OIL_PRODUCING_REGIONS_BY_COUNTRY = {
    "Spain": ["Andalusia", "Catalonia", "Castile-La Mancha", "Extremadura", "Valencia"],
    "Italy": ["Tuscany", "Sicily", "Puglia", "Calabria", "Lazio"],
    "Greece": ["Crete", "Peloponnese", "Lesbos", "Macedonia", "Thessaly"],
    "Turkiye": ["Aegean", "Marmara", "Mediterranean", "Southeastern Anatolia", "Central Anatolia"],
    "Tunisia": ["Sfax", "Kairouan", "Sousse", "Gabès", "Medenine"],
    "Portugal": ["Alentejo", "Trás-os-Montes", "Beira Interior", "Ribatejo", "Douro"],
    "Morocco": ["Meknes", "Fès", "Taza", "Tanger-Tetouan", "Tadla-Azilal"],
    "Syria": ["Idlib", "Aleppo", "Hama", "Latakia", "Daraa"],
    "Egypt": ["Marsa Matruh", "Alexandria", "Siwa Oasis", "Giza", "Ismailia"],
    "Algeria": ["Kabylie", "Tizi Ouzou", "Batna", "Constantine", "Setif"],
    "Lebanon": ["North Lebanon", "South Lebanon", "Bekaa Valley", "Mount Lebanon", "Nabatieh"],
    "Jordan": ["Irbid", "Ajloun", "Balqa", "Jerash", "Amman"],
    "Argentina": ["Mendoza", "San Juan", "La Rioja", "Catamarca", "Cordoba"],
    "Chile": ["Valparaíso", "O'Higgins", "Maule", "Metropolitana", "Ñuble"],
    "United States": ["California", "Texas", "Georgia", "Arizona", "Oregon"],
    "Australia": ["Victoria", "New South Wales", "South Australia", "Western Australia", "Tasmania"],
    "Other": ["Other"]
}

OLIVE_OIL_PRODUCING_COUNTRIES = list(OLIVE_OIL_PRODUCING_REGIONS_BY_COUNTRY.keys())

OLIVE_COLORS = [
    "Green", 
    "Black", 
    "Purple", 
    "Brown",
    "Yellow",
    "Red",
    "Other"
]

OLIVE_RARITIES = [
    "Widespread",
    "Regional",
    "Heritage",
    "Endangered",
    "Experimental"
]

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    _password = db.Column(db.String, nullable=False)

    oils = db.relationship('OliveOil', back_populates='user', cascade='all, delete-orphan')

    @property
    def producers(self):
        return list({oil.producer for oil in self.oils})

    @property
    def olives(self):
        return list({oil.olive for oil in self.oils})

    @hybrid_property
    def password(self):
        raise AttributeError('Password hashes may not be viewed.')

    @password.setter
    def password(self, password):
        if password is None or not isinstance(password, str) or not re.match(
            r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password
        ):
            raise ValueError("Password must be a non-empty string of at least 8 characters and include an uppercase letter, a lowercase letter, a number, and a special character.")

        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password = password_hash.decode('utf-8')

    def authenticate(self, password):
        try:
            return bcrypt.check_password_hash(self._password, password.encode('utf-8'))
        except ValueError as e:
            raise ValueError(f"Password hash is invalid: {self._password}") from e

    @validates('username')
    def validate_username(self, key, username):
        if username is None or not isinstance(username, str) or not re.match(r"^[a-zA-Z0-9]{6,16}$", username):
            raise ValueError("Username must be a non-empty string of at least 6 and at most 16 alphanumeric characters.")
        return username

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

    @validates('name')
    def validate_name(self, key, name):
        if name is None or not isinstance(name, str) or not re.match(r"^[a-zA-Z0-9 ]{3,}$", name):
            raise ValueError("Name must be a non-empty string of at least 3 characters.")
        return name

    @validates('country')
    def validate_country(self, key, country):
        if country not in OLIVE_OIL_PRODUCING_COUNTRIES:
            raise ValueError(f"Country must be one of {OLIVE_OIL_PRODUCING_COUNTRIES}.")
        return country

    @validates('region')
    def validate_region(self, key, region):
        all_regions = {region for regions in OLIVE_OIL_PRODUCING_REGIONS_BY_COUNTRY.values() for region in regions}

        if region not in all_regions:
            raise ValueError(f"Region must be one of {sorted(all_regions)}.")

        return region

    @validates('color')
    def validate_color(self, key, color):
        if color not in OLIVE_COLORS:
            raise ValueError(f"Color must be one of {OLIVE_COLORS}.")
        return color

    @validates('rarity')
    def validate_rarity(self, key, rarity):
        if rarity not in OLIVE_RARITIES:
            raise ValueError(f"Rarity must be one of {OLIVE_RARITIES}.")
        return rarity

    def __repr__(self):
        return f'<Olive id={self.id} name={self.name}>'

class Producer(db.Model):
    __tablename__ = "producers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    address = db.Column(db.String, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)

    oils = db.relationship('OliveOil', back_populates='producer', cascade='all, delete-orphan')

    @validates('name')
    def validate_name(self, key, name):
        if name is None or not isinstance(name, str) or not re.match(r"^[a-zA-Z0-9 ]{3,}$", name):
            raise ValueError("Name must be a non-empty string of at least 3 alphanumeric characters.")
        return name

    @validates('address')
    def validate_address(self, key, address):
        if address is None or not isinstance(address, str) or not re.match(r"^[a-zA-Z0-9 ]{12,}$", address):
            raise ValueError("Address must be a non-empty string of at least 12 characters.")
        return address

    @validates('capacity')
    def validate_capacity(self, key, capacity):
        if capacity is None or not isinstance(capacity, int) or capacity < 0:
            raise ValueError("Capacity must be a non-negative integer.")
        return capacity

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

    @validates('name')
    def validate_name(self, key, name):
        if name is None or not isinstance(name, str) or not re.match(r"^[a-zA-Z0-9 ]{3,}$", name):
            raise ValueError("Name must be a non-empty string of at least 3 characters.")
        return name

    @validates('year')
    def validate_year(self, key, year):
        if year is None or not isinstance(year, int) or not (1900 <= year <= 2025):
            raise ValueError("Year must be an integer between 1900 and 2025.")
        return year

    @validates('price')
    def validate_price(self, key, price):
        if price is None or not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a non-negative float.")
        return price

    @validates('isActive')
    def validate_isActive(self, key, isActive):
        if isActive is None or not isinstance(isActive, bool):
            raise ValueError("isActive must be a boolean.")
        return isActive

    @validates('acidity')
    def validate_acidity(self, key, acidity):
        if acidity is None or not isinstance(acidity, (int, float)) or not (0.0 <= acidity <= 3.0):
            raise ValueError("Acidity must be a float between 0.0 and 3.0.")
        return acidity

    def __repr__(self):
        return f'<OliveOil id={self.id} name={self.name}>'
