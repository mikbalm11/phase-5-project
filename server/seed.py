from config import app, db, bcrypt
from models import User, Olive, Producer, OliveOil
import random
from faker import Faker

fake = Faker()

with app.app_context():
    print("Resetting database...")
    db.drop_all()
    db.create_all()

    # --- Seed Users ---
    print("Seeding users...")
    user_data = [
        ("ikbal", "password"),
        ("alice", "password"),
        ("bob", "password"),
        ("charlie", "password"),
        ("diana", "password"),
        ("eve", "password"),
        ("olivefan", "password123"),
        ("tastetester", "securepass"),
    ]

    users = []
    for username, pw in user_data:
        user = User(username=username)
        user.password = pw
        db.session.add(user)
        users.append(user)
        print(f"Added user: {username}")

    db.session.commit()

    # --- Seed Olives ---
    print("Seeding olives...")
    base_olives = [
        Olive(name='Koroneiki', country='Greece', region='Crete', color='Green', rarity='Common'),
        Olive(name='Arbequina', country='Spain', region='Catalonia', color='Black', rarity='Uncommon'),
        Olive(name='Picual', country='Spain', region='Andalusia', color='Green', rarity='Rare'),
    ]

    colors = ['Green', 'Black', 'Purple']
    rarities = ['Common', 'Uncommon', 'Rare', 'Very Rare']
    countries = ['Greece', 'Spain', 'Italy', 'Turkiye', 'Morocco']
    regions = ['Crete', 'Catalonia', 'Andalusia', 'Sicily', 'Aegean']

    print("Generating unique olive names...")
    olive_names = set()
    generated_olives = []

    while len(generated_olives) < 25:
        name = f"{fake.unique.word().capitalize()} Olive"
        if name not in olive_names:
            olive_names.add(name)
            olive = Olive(
                name=name,
                country=random.choice(countries),
                region=random.choice(regions),
                color=random.choice(colors),
                rarity=random.choice(rarities)
            )
            generated_olives.append(olive)

    olives = base_olives + generated_olives
    db.session.add_all(olives)
    db.session.commit()

    # --- Seed Producers ---
    print("Seeding producers...")
    base_producers = [
        Producer(name='Golden Press', address='123 Olive Ln, Athens, Greece', capacity=5000),
        Producer(name='Verdant Oils', address='789 Grove Rd, Jaen, Spain', capacity=7000),
    ]

    generated_producers = [
        Producer(
            name=f"{fake.company()} Press",
            address=fake.address().replace("\n", ", "),
            capacity=random.randint(1000, 10000)
        ) for _ in range(10)
    ]

    producers = base_producers + generated_producers
    db.session.add_all(producers)
    db.session.commit()

    # --- Seed Olive Oils ---
    print("Seeding olive oils...")
    base_oils = [
        OliveOil(name='Aegean Gold', year=2023, price=25.99, isActive=True, acidity=0.3,
                 user_id=users[6].id, producer_id=producers[0].id, olive_id=olives[0].id),
        OliveOil(name='Catalan Reserve', year=2022, price=29.99, isActive=True, acidity=0.2,
                 user_id=users[7].id, producer_id=producers[1].id, olive_id=olives[1].id),
        OliveOil(name='Andalusian Pure', year=2024, price=32.50, isActive=False, acidity=0.1,
                 user_id=users[6].id, producer_id=producers[1].id, olive_id=olives[2].id),
    ]

    generated_oils = [
        OliveOil(
            name=f"{fake.color_name()} Reserve",
            year=random.choice([2021, 2022, 2023, 2024]),
            price=round(random.uniform(15.0, 45.0), 2),
            isActive=random.choice([True, False]),
            acidity=round(random.uniform(0.1, 0.5), 2),
            user_id=random.choice(users).id,
            producer_id=random.choice(producers).id,
            olive_id=random.choice(olives).id
        ) for _ in range(25)
    ]

    db.session.add_all(base_oils + generated_oils)
    db.session.commit()

    print("Seeding complete.")
