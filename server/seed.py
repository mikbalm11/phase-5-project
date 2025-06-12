from config import app, db, bcrypt
from models import User, Olive, Producer, OliveOil, OLIVE_OIL_PRODUCING_REGIONS_BY_COUNTRY, OLIVE_COLORS, OLIVE_RARITIES
import random
from faker import Faker
import re

fake = Faker()

def valid_password():
    """Generate a valid password according to your regex:
    At least 8 chars, including uppercase, lowercase, digit, special char"""
    # We'll ensure it meets the regex: 
    # r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    # We'll create a random password with at least one from each category

    specials = "@$!%*?&"
    password_chars = [
        random.choice("abcdefghijklmnopqrstuvwxyz"),  # lowercase
        random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),  # uppercase
        random.choice("0123456789"),                 # digit
        random.choice(specials)                      # special char
    ]
    # Fill the rest with random allowed chars
    while len(password_chars) < 10:
        password_chars.append(random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" + specials))
    random.shuffle(password_chars)
    return ''.join(password_chars)

def valid_username(base):
    """Generate a valid username (6-16 alphanumeric chars) based on base string"""
    username = re.sub(r'\W+', '', base)  # remove non-alphanumeric
    username = username[:16]  # truncate max length 16
    if len(username) < 6:
        username += "User"  # pad to min length 6 if needed
    return username

def valid_address():
    # At least 12 characters, alphanumeric and spaces allowed.
    # We'll generate a fake address and remove problematic chars.
    
    addr = fake.address().replace("\n", ", ")
    # Keep only alphanumeric, spaces, commas
    addr = re.sub(r'[^a-zA-Z0-9 ,]', '', addr)
    if len(addr) < 12:
        addr += " 1234"
    return addr

with app.app_context():
    print("Resetting database...")
    db.drop_all()
    db.create_all()

    # --- Seed Users ---
    print("Seeding users...")
    # Your user_data usernames are mostly invalid due to new rules (min 6 chars + alphanumeric)
    # We'll fix them or generate new valid usernames with valid passwords

    raw_usernames = [
        "ikbal", "alice", "bob", "charlie", "diana", "eve", "olivefan", "tastetester"
    ]
    users = []

    for base_name in raw_usernames:
        username = valid_username(base_name)
        user = User(username=username)
        # Assign a valid random password to satisfy validation rules
        pw = valid_password()
        try:
            user.password = pw
            db.session.add(user)
            users.append(user)
            print(f"Added user: {username} with password: {pw}")
        except ValueError as e:
            print(f"Failed to add user {username}: {e}")

    db.session.commit()

    # --- Seed Olives ---
    print("Seeding olives...")

    all_regions = [region for regions in OLIVE_OIL_PRODUCING_REGIONS_BY_COUNTRY.values() for region in regions]
    all_countries = list(OLIVE_OIL_PRODUCING_REGIONS_BY_COUNTRY.keys())

    base_olives = [
        Olive(name='Koroneiki', country='Greece', region='Crete', color='Green', rarity='Regional'),
        Olive(name='Arbequina', country='Spain', region='Catalonia', color='Black', rarity='Widespread'),
        Olive(name='Picual', country='Spain', region='Andalusia', color='Green', rarity='Heritage'),
    ]

    olive_names = set(o.name for o in base_olives)
    generated_olives = []

    while len(generated_olives) < 50:
        name = f"{fake.unique.word().capitalize()} Olive"
        if name not in olive_names:
            olive_names.add(name)
            country = random.choice(all_countries)
            region = random.choice(OLIVE_OIL_PRODUCING_REGIONS_BY_COUNTRY[country])
            color = random.choice(OLIVE_COLORS[:-1])  # exclude 'Other'
            rarity = random.choice(OLIVE_RARITIES[:-1])  # exclude 'Experimental'
            try:
                olive = Olive(
                    name=name,
                    country=country,
                    region=region,
                    color=color,
                    rarity=rarity
                )
                generated_olives.append(olive)
            except ValueError as e:
                print(f"Skipping invalid olive: {name} - {e}")

    olives = base_olives + generated_olives
    db.session.add_all(olives)
    db.session.commit()

    # --- Seed Producers ---
    print("Seeding producers...")

    base_producers = [
        Producer(name='Golden Press', address='123 Olive Ln, Athens, Greece', capacity=5000),
        Producer(name='Verdant Oils', address='789 Grove Rd, Jaen, Spain', capacity=7000),
    ]

    generated_producers = []
    producer_names = set(p.name for p in base_producers)

    while len(generated_producers) < 50:
        name = f"{fake.company()} Press"
        # Clean the name to fit validation (3+ alphanumeric and spaces)
        name = re.sub(r'[^a-zA-Z0-9 ]', '', name)
        if name not in producer_names and len(name) >= 3:
            producer_names.add(name)
            address = valid_address()
            capacity = random.randint(1000, 10000)
            try:
                producer = Producer(name=name, address=address, capacity=capacity)
                generated_producers.append(producer)
            except ValueError as e:
                print(f"Skipping invalid producer: {name} - {e}")

    producers = base_producers + generated_producers
    db.session.add_all(producers)
    db.session.commit()

    # --- Seed Olive Oils ---
    print("Seeding olive oils...")

    base_oils = [
        OliveOil(
            name='Aegean Gold', year=2023, price=25.99, isActive=True, acidity=0.3,
            user_id=users[6].id, producer_id=producers[0].id, olive_id=olives[0].id
        ),
        OliveOil(
            name='Catalan Reserve', year=2022, price=29.99, isActive=True, acidity=0.2,
            user_id=users[7].id, producer_id=producers[1].id, olive_id=olives[1].id
        ),
        OliveOil(
            name='Andalusian Pure', year=2024, price=32.50, isActive=False, acidity=0.1,
            user_id=users[6].id, producer_id=producers[1].id, olive_id=olives[2].id
        ),
    ]

    generated_oils = []
    for _ in range(100):
        name = f"{fake.color_name()} Reserve"
        # Clean name to fit validation
        name = re.sub(r'[^a-zA-Z0-9 ]', '', name)
        if len(name) < 3:
            name = "Reserve Oil"

        year = random.randint(1900, 2025)
        price = round(random.uniform(10.0, 50.0), 2)
        is_active = random.choice([True, False])
        acidity = round(random.uniform(0.0, 3.0), 2)

        user = random.choice(users)
        producer = random.choice(producers)
        olive = random.choice(olives)

        try:
            oil = OliveOil(
                name=name,
                year=year,
                price=price,
                isActive=is_active,
                acidity=acidity,
                user_id=user.id,
                producer_id=producer.id,
                olive_id=olive.id
            )
            generated_oils.append(oil)
        except ValueError as e:
            print(f"Skipping invalid olive oil: {name} - {e}")

    db.session.add_all(base_oils + generated_oils)
    db.session.commit()

    print("Seeding complete.")
