#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from logging import getLogger
from random import randint

from forgery_py.forgery.basic import text, hex_color, hex_color_short
from forgery_py.forgery.internet import user_name
from forgery_py.forgery.name import full_name
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from models.taxi import Users, Vehicles, association

logger = getLogger(__name__)


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

    def generate_user(self):
        login = user_name()
        if login not in self.LOGINS:
            user = Users(
                name=full_name(),
                login=login,
                password=text(8),
            )
            self.LOGINS.append(login)
            vehicles = []
            for _ in range(randint(1, 5)):
                vehicle_id = randint(1, 10)
                vehicle = self.session.query(Vehicles).filter(Vehicles.id == vehicle_id).first()
                if vehicle not in vehicles:
                    vehicles.append(vehicle)
            user.vehicles = vehicles
            logger.info('User was generated. Name: {}, login: {}, password: {}. Vehicles: {}'.format(
                user.name,
                user.login,
                user.password,
                str([vehicle.id for vehicle in user.vehicles]).strip('[]')))
            return user

    def generate_vehicle(self):
        title = hex_color()
        if title not in self.TITLES:
            vehicle = Vehicles(
                title=title,
                type=hex_color_short(),
                price=randint(1000, 1000000)
            )
            self.TITLES.append(title)
            logger.info('Vehicle was generated. Title: {}, type: {}, price: {}.'.format(
                vehicle.title,
                vehicle.type,
                vehicle.price))
            return vehicle

    def generate_data(self):
        self.base.metadata.drop_all(tables=[Users.__table__, Vehicles.__table__, association])
        self.base.metadata.create_all(tables=[Users.__table__, Vehicles.__table__, association])

        while len(self.session.query(Vehicles).all()) < 10:
            vehicle = self.generate_vehicle()
            if vehicle is not None:
                self.session.add(vehicle)

        while len(self.session.query(Users).all()) < 100:
            user = self.generate_user()
            if user is not None:
                self.session.add(user)

        self.session.commit()

    def generate_samples(self):
        self.SAMPLE_1 = self.session.query(Users.id, Users.name).filter(Users.id == randint(1, 100)).first()
        self.SAMPLE_2 = self.session.query(Users.name, Users.login).filter(Users.id == randint(1, 100)).first()
        self.SAMPLE_3 = self.session.query(Users.login, Users.name).filter(Users.id == randint(1, 100)).first()
        self.SAMPLE_4 = self.session.query(Users.id, Users.login).filter(Users.id == randint(1, 100)).first()
        self.SAMPLE_5 = self.session.query(Users.id, Users.password).filter(Users.id == randint(1, 100)).first()

        sample_6_id = randint(1, 100)
        vehicles = self.session.query(Users).filter(Users.id == sample_6_id).first().vehicles
        sample_6_ids = [vehicle.id for vehicle in vehicles]
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
        users = self.session.query(Vehicles).filter(Vehicles.id == sample_13_1_id).first().users
        sample_13_1_ids = [user.id for user in users]
        self.SAMPLE_13_1 = (
            sample_13_1_id,
            sample_13_1_ids
        )

        sample_13_2_vehicle = self.session.query(Vehicles).filter(Vehicles.id == randint(1, 10)).first()
        sample_13_2_ids = [user.id for user in sample_13_2_vehicle.users]
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

        sample_15_user = None
        while sample_15_user is None:
            sample_15_user = self.generate_user()
        self.SAMPLE_15 = (
            sample_15_user.name,
            sample_15_user.login,
            sample_15_user.password,
            [vehicle.id for vehicle in sample_15_user.vehicles]
        )

        sample_16_vehicle = None
        while sample_16_vehicle is None:
            sample_16_vehicle = self.generate_vehicle()
        sample_16_vehicle.users = [
            self.session.query(Users).filter(Users.id == randint(1, 100)).first() for _ in range(randint(1, 20))
        ]
        self.SAMPLE_16 = (
            sample_16_vehicle.title,
            sample_16_vehicle.type,
            sample_16_vehicle.price,
            [user.id for user in sample_16_vehicle.users]
        )
