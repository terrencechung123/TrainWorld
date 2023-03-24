#!/usr/bin/env python3

from random import randint, choice as rc

from faker import Faker

from app import app
from models import db, Train, User

fake = Faker()

with app.app_context():

    print("Deleting all records...")
    Train.query.delete()
    User.query.delete()

    fake = Faker()

    print("Creating users...")

    # make sure users have unique usernames
    users = []
    usernames = []

    for i in range(20):
        
        username = fake.first_name()
        while username in usernames:
            username = fake.first_name()
        usernames.append(username)

        user = User(
            username=username,
            bio=fake.paragraph(nb_sentences=3),
            image_url=fake.url(),
        )

        user.password_hash = user.username + 'password'

        users.append(user)

    db.session.add_all(users)

    print("Creating trains...")
    trains = []
    for i in range(100):
        instructions = fake.paragraph(nb_sentences=8)
        
        train = Train(
            title=fake.sentence(),
            instructions=instructions,
            minutes_to_complete=randint(15,90),
        )

        train.user = rc(users)

        trains.append(train)

    db.session.add_all(trains)
    
    db.session.commit()
    print("Complete.")
