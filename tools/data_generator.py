#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from random import randint

import forgery_py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models.taxi import Users, Vehicles, association

logger = logging.getLogger(__name__)


class DataGenerator(object):

    LOGINS = []
    TITLES = []
    SAMPLE_1 = None
    SAMPLE_2 = None
    SAMPLE_3 = None
    SAMPLE_4 = None
    SAMPLE_5 = None
    SAMPLE_6 = None
    SAMPLE_7 = None
    SAMPLE_8 = None
    SAMPLE_9_1 = None
    SAMPLE_9_2 = None
    SAMPLE_10_1 = None
    SAMPLE_10_2 = None
    SAMPLE_11 = None
    SAMPLE_12_1 = None
    SAMPLE_12_2 = None
    SAMPLE_13_1 = None
    SAMPLE_13_2 = None
    SAMPLE_14 = None
    SAMPLE_15 = None
    SAMPLE_16 = None

    def __init__(self, db_name, username, password, db_type='postgresql', dbapi='psycopg2', host='127.0.0.1',
                 port='5432', log=False):

        self.engine = create_engine('{}+{}://{}:{}@{}:{}/{}'.format(
            db_type,
            dbapi,
            username,
            password,
            host,
            port,
            db_name
        ), echo=log)
        self.session = sessionmaker(bind=self.engine)()
        self.base = declarative_base(bind=self.engine)

    def generate_data(self):

        self.base.metadata.drop_all(tables=[Users.__table__, Vehicles.__table__, association])
        self.base.metadata.create_all(tables=[Users.__table__, Vehicles.__table__, association])

        while len(self.session.query(Users).all()) < 100:
            login = forgery_py.internet.user_name()
            if login in self.LOGINS:
                continue
            user = Users(
                name=forgery_py.name.full_name(),
                login=login,
                password=forgery_py.basic.text(8),
            )
            self.LOGINS.append(login)
            self.session.add(user)

        while len(self.session.query(Vehicles).all()) < 10:
            title = forgery_py.basic.hex_color()
            if title in self.TITLES:
                continue
            vehicle = Vehicles(
                title=title,
                type=forgery_py.basic.hex_color_short(),
                price=randint(1000, 1000000)
            )
            self.TITLES.append(title)
            self.session.add(vehicle)

        for user in self.session.query(Users):
            vehicles = []
            for i in range(randint(1, 5)):
                vehicle_id = randint(1, 10)
                vehicle = self.session.query(Vehicles).filter(Vehicles.id == vehicle_id).first()
                if vehicle not in vehicles:
                    vehicles.append(vehicle)
            user.vehicles = vehicles
            self.session.add(user)

        for user_id, name, login, password in self.session.query(Users.id, Users.name, Users.login, Users.password):
            logger.info('{} {} {} {}'.format(user_id, name.rstrip(), login.rstrip(), password.rstrip()))

        for vehicle_id, title, vehicle_type, price in self.session.query(Vehicles.id, Vehicles.title, Vehicles.type,
                                                                         Vehicles.price):
            logger.info('{} {} {} {}'.format(vehicle_id, title.rstrip(), vehicle_type.rstrip(), price))

        for user_id, user in self.session.query(Users.id, Users).order_by(Users.id):
            logger.info('User ID: {}'.format(user_id))
            for vehicle in user.vehicles:
                logger.info('\tVehicle ID: {}'.format(vehicle.id))

        self.session.commit()

    def generate_samples(self):

        self.SAMPLE_1 = self.session.query(Users.id, Users.name).filter(Users.id == randint(1, 100)).first()
        self.SAMPLE_2 = self.session.query(Users.name, Users.login).filter(Users.id == randint(1, 100)).first()
        self.SAMPLE_3 = self.session.query(Users.login, Users.name).filter(Users.id == randint(1, 100)).first()
        self.SAMPLE_4 = self.session.query(Users.id, Users.login).filter(Users.id == randint(1, 100)).first()
        self.SAMPLE_5 = self.session.query(Users.id, Users.password).filter(Users.id == randint(1, 100)).first()

        sample_6_id = randint(1, 100)
        sample_6_ids = []
        for vehicle in self.session.query(Users).filter(Users.id == sample_6_id).first().vehicles:
            sample_6_ids.append(vehicle.id)
        self.SAMPLE_6 = (
            sample_6_id,
            sample_6_ids
        )

        self.SAMPLE_7 = self.session.query(Vehicles.id, Vehicles.title).filter(Vehicles.id == randint(1, 10)).first()
        self.SAMPLE_8 = self.session.query(Vehicles.title, Vehicles.id).filter(Vehicles.id == randint(1, 10)).first()
        self.SAMPLE_9_1 = self.session.query(Vehicles.id, Vehicles.title).filter(Vehicles.id == randint(1, 10)).first()
        self.SAMPLE_9_2 = self.session.query(Vehicles.title, Vehicles.id).filter(Vehicles.id == randint(1, 10)).first()
        self.SAMPLE_10_1 = self.session.query(Vehicles.id, Vehicles.type).filter(Vehicles.id == randint(1, 10)).first()
        self.SAMPLE_10_2 = self.session.query(Vehicles.title,
                                              Vehicles.type).filter(Vehicles.id == randint(1, 10)).first()
        self.SAMPLE_11 = self.session.query(Vehicles.type, Vehicles.id).filter(Vehicles.id == randint(1, 10)).first()
        self.SAMPLE_12_1 = self.session.query(Vehicles.id, Vehicles.price).filter(Vehicles.id == randint(1, 10)).first()
        self.SAMPLE_12_2 = self.session.query(Vehicles.title,
                                              Vehicles.price).filter(Vehicles.id == randint(1, 10)).first()

        sample_13_1_id = randint(1, 10)
        sample_13_1_ids = []
        for user in self.session.query(Vehicles).filter(Vehicles.id == sample_13_1_id).first().users:
            sample_13_1_ids.append(user.id)
        self.SAMPLE_13_1 = (
            sample_13_1_id,
            sample_13_1_ids
        )

        sample_13_2_vehicle = self.session.query(Vehicles).filter(Vehicles.id == randint(1, 10)).first()
        sample_13_2_ids = []
        for user in sample_13_2_vehicle.users:
            sample_13_2_ids.append(user.id)
        self.SAMPLE_13_2 = (
            sample_13_2_vehicle.title,
            sample_13_2_ids
        )

        sample_14 = self.session.query(Users).filter(Users.id == randint(1, 100)).first()
        total_price = 0
        for vehicle in sample_14.vehicles:
            total_price += vehicle.price
        self.SAMPLE_14 = (
            sample_14.id,
            total_price
        )

        sample_15_name = forgery_py.name.full_name()
        sample_15_login = None
        sample_15_password = forgery_py.basic.text(8)
        sample_15_vehicles = list(randint(1, 10) for _ in range(randint(1, 5)))
        while sample_15_login is None:
            login = forgery_py.internet.user_name()
            if login not in self.LOGINS:
                sample_15_login = login
                self.LOGINS.append(login)
        self.SAMPLE_15 = (
            sample_15_name,
            sample_15_login,
            sample_15_password,
            sample_15_vehicles
        )

        sample_16_title = None
        sample_16_type = forgery_py.basic.hex_color_short()
        sample_16_price = randint(1000, 1000000)
        sample_16_users = list(randint(1, 100) for _ in range(randint(1, 20)))
        while sample_16_title is None:
            title = forgery_py.basic.hex_color()
            if title not in self.TITLES:
                sample_16_title = title
                self.TITLES.append(title)
        self.SAMPLE_16 = (
            sample_16_title,
            sample_16_type,
            sample_16_price,
            sample_16_users
        )
