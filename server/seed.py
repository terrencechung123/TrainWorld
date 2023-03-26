#!/usr/bin/env python3

from random import randint, choice as rc

from faker import Faker

from app import app
from models import db, Ticket, User, Train

fake = Faker()

with app.app_context():

    print("Deleting all records...")
    Ticket.query.delete()
    User.query.delete()


    fake = Faker()

    print("Creating users...")

    # make sure users have unique usernames
    users = []
    usernames = []

    for i in range(10):

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
    for i in range(5):
        train = Train(
            title = fake.first_name(),
            description = f'Starting Destination: {fake.first_name()}, Ending Destination: {fake.first_name()}',
            image_url = fake.url()
        )
        trains.append(train)
    db.session.add_all(trains)

    print("Creating tickets...")
    tickets = []
    for i in range(10):
        # instructions = fake.paragraph(nb_sentences=8)

        ticket = Ticket(
            price=20
            )

        ticket.user = rc(users)
        ticket.train = rc(trains)
        tickets.append(ticket)

    db.session.add_all(tickets)

    db.session.commit()
    print("Complete.")


    # for i in range(5):
    #     ticket = Ticket()
    #     ticket.user = rc(users)
    #     tickets.append(ticket)
    # california = Ticket(
    #     price="California",
    #     description=' With its large population and extensive rail network, California is one of the most popular states for train travel in the US. Amtrak\'s Pacific Surfliner, Capitol Corridor, and San Joaquin lines are particularly popular.'
    #     )
    # newyork = Ticket(
    #     price="New York",
    #     description='New York is home to one of the largest and oldest subway systems in the world, as well as several commuter rail systems. Trains are a crucial mode of transportation for the millions of people who live and work in the New York City area.'
    #     )
    # illinois = Ticket(
    #     price = "Illinois",
    #     description= 'Illinois is a hub for rail transportation in the Midwest, with Amtrak\'s high-speed Acela Express and several commuter rail lines serving the Chicago area.'
    # )
    # texas = Ticket(
    #     price = "Texas",
    #     description = 'Illinois is a hub for rail transportation in the Midwest, with Amtrak\'s high-speed Acela Express and several commuter rail lines serving the Chicago area.'
    # )
    # washington = Ticket(
    #     price = "Washington",
    #     description = 'With its scenic views and extensive rail network, Washington is a popular destination for train travel. Amtrak\'s Cascades line and Sound Transit\'s commuter rail system are particularly popular.'
    # )
