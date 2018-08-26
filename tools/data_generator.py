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

logins = []
while len(session.query(Users).all()) < 100:
    login = forgery_py.internet.user_name()
    if login in logins:
        continue
    user = Users(
        name=forgery_py.name.full_name(),
        login=login,
        password=forgery_py.basic.text(8),
    )
    logins.append(login)
    session.add(user)

titles = []
while len(session.query(Vehicles).all()) < 10:
    title = forgery_py.basic.hex_color()
    if title in titles:
        continue
    vehicle = Vehicles(
        title=title,
        type=forgery_py.basic.hex_color_short(),
        price=random.randint(1000, 1000000)
    )
    titles.append(title)
    session.add(vehicle)

for user in session.query(Users):
    vehicles = []
    for i in range(random.randint(1, 5)):
        vehicle_id = random.randint(1, 10)
        vehicle = session.query(Vehicles).filter(Vehicles.id == vehicle_id).first()
        if vehicle not in vehicles:
            vehicles.append(vehicle)
    user.vehicles = vehicles
    session.add(user)

for user_id, name, login, password in session.query(Users.id, Users.name, Users.login, Users.password):
    print('{} {} {} {}'.format(user_id, name.rstrip(), login.rstrip(), password.rstrip()))

print()

for vehicle_id, title, vtype, price in session.query(Vehicles.id, Vehicles.title, Vehicles.type, Vehicles.price):
    print('{} {} {} {}'.format(vehicle_id, title.rstrip(), vtype.rstrip(), price))

print()

for user_id, user in session.query(Users.id, Users).order_by(Users.id):
    print('User ID: {}'.format(user_id))
    for vehicle in user.vehicles:
        print('\tVehicle ID: {}'.format(vehicle.id))

session.commit()
