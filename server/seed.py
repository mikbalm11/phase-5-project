from config import app, db, bcrypt
from models import User, Olive, Producer, OliveOil

# Clear existing data
with app.app_context():
    print("Clearing database...")
    db.drop_all()
    db.create_all()

    # Create users
    print("Seeding users...")
    user1 = User(username='olivefan')
    user1._password = bcrypt.generate_password_hash('password123').decode('utf-8')

    user2 = User(username='tastetester')
    user2._password = bcrypt.generate_password_hash('securepass').decode('utf-8')

    db.session.add_all([user1, user2])
    db.session.commit()

    # Create olives
    print("Seeding olives...")
    olive1 = Olive(name='Koroneiki', country='Greece', region='Crete', color='Green', rarity='Common')
    olive2 = Olive(name='Arbequina', country='Spain', region='Catalonia', color='Black', rarity='Uncommon')
    olive3 = Olive(name='Picual', country='Spain', region='Andalusia', color='Green', rarity='Rare')

    db.session.add_all([olive1, olive2, olive3])
    db.session.commit()

    # Create producers
    print("Seeding producers...")
    producer1 = Producer(name='Golden Press', address='123 Olive Ln, Athens, Greece', capacity=5000)
    producer2 = Producer(name='Verdant Oils', address='789 Grove Rd, Jaen, Spain', capacity=7000)

    db.session.add_all([producer1, producer2])
    db.session.commit()

    # Create olive oils
    print("Seeding olive oils...")
    oil1 = OliveOil(name='Aegean Gold', year=2023, price=25.99, isActive=True, acidity=0.3,
                    user_id=user1.id, producer_id=producer1.id, olive_id=olive1.id)

    oil2 = OliveOil(name='Catalan Reserve', year=2022, price=29.99, isActive=True, acidity=0.2,
                    user_id=user2.id, producer_id=producer2.id, olive_id=olive2.id)

    oil3 = OliveOil(name='Andalusian Pure', year=2024, price=32.50, isActive=False, acidity=0.1,
                    user_id=user1.id, producer_id=producer2.id, olive_id=olive3.id)

    db.session.add_all([oil1, oil2, oil3])
    db.session.commit()

    print("Seeding complete.")
