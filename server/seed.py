#!/usr/bin/env python3
from random import choice as rc
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import app
from models import db, Conductor, Train, TrainRide

with app.app_context():

# This will delete any existing rows
# so you can run the seed file multiple times without having duplicate entries in your database
    print("Deleting data...")
    Train.query.delete()
    Conductor.query.delete()
    TrainRide.query.delete()

    print("Creating conductors...")
    conductor1 = Conductor(name = "Bob", avatar = 'avatar1')#change avatar pictures later
    conductor2 = Conductor(name = "Bill", avatar = 'avatar2')
    conductor3 = Conductor(name = "Bo", avatar = 'avatar3')
    conductors = [conductor1, conductor2, conductor3]

    print("Creating trains...")


    train1 = Train(name = "Thomas", description = "The Train Engine", avatar = 'avatar1')
    train2 = Train(name = "Percy", description = "The Green Train", avatar = 'avatar2')
    train3 = Train(name = "Toby", description = "The Tram Engine", avatar = 'avatar3')
    trains = [train1,train2,train3]

    print("Creating TrainRide...")

    tr1 = TrainRide(conductor = conductor1, train = train1)
    tr2 = TrainRide(conductor = conductor2, train  = train2)
    tr3 = TrainRide(conductor = conductor3, train = train3)
    trainRides = [tr1, tr2, tr3]
    db.session.add_all(conductors)
    db.session.add_all(trains)
    db.session.add_all(trainRides)
    db.session.commit()

    print("Seeding done!")