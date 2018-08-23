#!/usr/bin/env python3
# -*- coding: ascii -*-
import os
import random
import sys

sys.path.append(os.path.abspath('.'))

from config import SSH

import forgery_py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models.taxi import Users, Vehicles, association

engine = create_engine('postgresql+psycopg2://{}:{}@192.168.56.101:5432/test_db'.format(SSH.USERNAME, SSH.PASSWORD))
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base(bind=engine)
Base.metadata.drop_all(tables=[Users.__table__, Vehicles.__table__, association])
Base.metadata.create_all(tables=[Users.__table__, Vehicles.__table__, association])

for i in range(100):
    user = Users(
        name=forgery_py.name.full_name(),
        login=forgery_py.internet.user_name(),
        password=forgery_py.basic.text(8),
    )
    session.add(user)

for i in range(10):
    vehicle = Vehicles(
        title=forgery_py.basic.hex_color(),
        type=forgery_py.basic.hex_color_short(),
        price=random.randint(1000, 1000000)
    )
    session.add(vehicle)

for user in session.query(Users):
    vehicles = []
    for i in range(random.randint(1, 5)):
        vehicle_id = random.randint(1, 10)
        vehicle = session.query(Vehicles).filter(Vehicles.id == vehicle_id).first()
        vehicles.append(vehicle)
    user.vehicles = vehicles
    session.add(user)

for user_id, name, login, password in session.query(Users.id, Users.name, Users.login, Users.password):
    print('{} {} {} {}'.format(user_id, name.rstrip(), login.rstrip(), password.rstrip()))

print()

for vehicle_id, title, vtype, price in session.query(Vehicles.id, Vehicles.title, Vehicles.type, Vehicles.price):
    print('{} {} {} {}'.format(vehicle_id, title.rstrip(), vtype.rstrip(), price))

print()

for vehicle_id, vehicle in session.query(Vehicles.id, Vehicles).order_by(Vehicles.id):
    print('Vehicle ID: {}'.format(vehicle_id))
    for user in vehicle.users:
        print('\tUser ID: {}'.format(user.id))

print()

for user_id, user in session.query(Users.id, Users).order_by(Users.id):
    print('User ID: {}'.format(user_id))
    for vehicle in user.vehicles:
        print('\tVehicle ID: {}'.format(vehicle.id))

session.commit()
