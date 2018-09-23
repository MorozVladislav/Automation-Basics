#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from logging import getLogger

from integration.db_client import DBClient
from models.taxi import Users, Vehicles

logger = getLogger(__name__)


class DBSteps(DBClient):

    def __init__(self, db_name, username, password, host='127.0.0.1', port='5432', autocomit=False, autoflush=True,
                 save_when_close=False, log=False):
        super().__init__(db_name, username, password, db_type='postgresql', dbapi='psycopg2', host=host, port=port,
                         autocomit=autocomit, autoflush=autoflush, save_when_close=save_when_close, log=log)

    def get_user_by_id(self, user_id):
        return self.query(Users).filter(Users.id == user_id).first()

    def get_users_by_name(self, username):
        return self.query(Users).filter(Users.name == username)

    def get_user_by_login(self, login):
        return self.query(Users).filter(Users.login == login).first()

    def get_user_login(self, user_id):
        return self.get_user_by_id(user_id).login

    def get_user_password(self, user_id):
        return self.get_user_by_id(user_id).password

    def get_user_vehicles(self, user_id):
        return self.get_user_by_id(user_id).vehicles

    def get_vehicle_by_id(self, vehicle_id):
        return self.query(Vehicles).filter(Vehicles.id == vehicle_id).first()

    def get_vehicle_by_title(self, title):
        return self.query(Vehicles).filter(Vehicles.title == title).first()

    def get_vehicle(self, vehicle_id=None, title=None):
        if vehicle_id is not None:
            return self.get_vehicle_by_id(vehicle_id)
        elif title is not None:
            return self.get_vehicle_by_title(title)
        else:
            message = 'Neither vehicle_id nor title are specified'
            logger.error(message)
            raise QueryParametersNotSpecified(message)

    def get_vehicle_type(self, vehicle_id=None, title=None):
        return self.get_vehicle(vehicle_id=vehicle_id, title=title).type

    def get_vehicles_by_type(self, vehicles_type):
        return self.query(Vehicles).filter(Vehicles.type == vehicles_type)

    def get_vehicle_price(self, vehicle_id=None, title=None):
        return self.get_vehicle(vehicle_id=vehicle_id, title=title).price

    def get_owners(self, vehicle_id=None, title=None):
        return self.get_vehicle(vehicle_id=vehicle_id, title=title).users

    def get_user_vehicles_total_price(self, user_id):
        total_price = 0
        for vehicle in self.get_user_by_id(user_id).vehicles:
            total_price += vehicle.price
        return total_price

    def add_user(self, username, login, password, vehicles=None):
        logins = [user.login for user in self.query(Users).all()]
        if login in logins:
            message = 'Login {} already exist'.format(login)
            logger.error(message)
            raise LoginAlreadyExist(message)
        user = Users()
        user.name, user.login, user.password = username, login, password
        user.vehicles = [value for value in set(vehicles) if vehicles is not None]
        self.add(user)
        logger.info('User {} was added'.format(username))

    def add_vehicle(self, title, vehicle_type, price, users=None):
        titles = [vehicle.title for vehicle in self.query(Vehicles).all()]
        if title in titles:
            message = 'Vehicle {} already exist'.format(title)
            logger.error(message)
            raise VehicleAlreadyExist(message)
        vehicle = Vehicles()
        vehicle.title, vehicle.type, vehicle.price = title, vehicle_type, price
        vehicle.users = [value for value in (set(users)) if users is not None]
        self.add(vehicle)
        logger.info('Vehicle {} was added'.format(title))

    def delete_user(self, user_id):
        user = self.get_user_by_id(user_id)
        self.delete(user)
        logger.info('User {} was deleted'.format(user.name))

    def delete_vehicle(self, vehicle_id=None, title=None):
        vehicle = self.get_vehicle(vehicle_id=vehicle_id, title=title)
        self.delete(vehicle)
        logger.info('Vehicle {} was deleted'.format(vehicle.title))


class DBStepsException(Exception):
    pass


class QueryParametersNotSpecified(DBStepsException):
    pass


class UserCreationError(DBStepsException):
    pass


class LoginAlreadyExist(DBStepsException):
    pass


class VehicleAlreadyExist(DBStepsException):
    pass
