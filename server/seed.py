from config import app, db, bcrypt
from models import User, Olive, Producer, OliveOil, OLIVE_OIL_PRODUCING_REGIONS_BY_COUNTRY, OLIVE_COLORS, OLIVE_RARITIES
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
        ("olivefan", "password"),
        ("tastetester", "password"),
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

    # Flatten all valid regions for validation
    all_regions = [region for regions in OLIVE_OIL_PRODUCING_REGIONS_BY_COUNTRY.values() for region in regions]
    all_countries = list(OLIVE_OIL_PRODUCING_REGIONS_BY_COUNTRY.keys())

    # Some base olives with valid rarity and colors from your constants
    base_olives = [
        Olive(name='Koroneiki', country='Greece', region='Crete', color='Green', rarity='Regional'),
        Olive(name='Arbequina', country='Spain', region='Catalonia', color='Black', rarity='Widespread'),
        Olive(name='Picual', country='Spain', region='Andalusia', color='Green', rarity='Heritage'),
    ]

    # Generate unique olive names avoiding collisions
    olive_names = set(o.name for o in base_olives)
    generated_olives = []

    while len(generated_olives) < 50:
        name = f"{fake.unique.word().capitalize()} Olive"
        if name not in olive_names:
            olive_names.add(name)
            country = random.choice(all_countries)
            region = random.choice(OLIVE_OIL_PRODUCING_REGIONS_BY_COUNTRY[country])
            color = random.choice(OLIVE_COLORS[:-1])  # exclude 'Other' for seeding realism
            rarity = random.choice(OLIVE_RARITIES[:-1])  # exclude 'Experimental' for seeding
            olive = Olive(
                name=name,
                country=country,
                region=region,
                color=color,
                rarity=rarity
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

    generated_producers = []
    producer_names = set(p.name for p in base_producers)

    while len(generated_producers) < 50:
        name = f"{fake.company()} Press"
        if name not in producer_names:
            producer_names.add(name)
            address = fake.address().replace("\n", ", ")
            capacity = random.randint(1000, 10000)
            producer = Producer(name=name, address=address, capacity=capacity)
            generated_producers.append(producer)

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
        year = random.randint(1900, 2025)
        price = round(random.uniform(10.0, 50.0), 2)
        is_active = random.choice([True, False])
        acidity = round(random.uniform(0.0, 3.0), 2)  # full valid range

        user = random.choice(users)
        producer = random.choice(producers)
        olive = random.choice(olives)

        # Create oil instance
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

    db.session.add_all(base_oils + generated_oils)
    db.session.commit()

    print("Seeding complete.")
