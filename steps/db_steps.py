#!/usr/bin/env python3
# -*- coding: ascii -*-
import logging

from integration.db_client import DBClient
from models.taxi import Users, Vehicles

logger = logging.getLogger(__name__)


def id_or_name(func):
    def wrapped(obj, user_id=None, username=None):

        if user_id is not None:
            return func(obj, user=obj.get_user_by_id(user_id))
        elif username is not None:
            return func(obj, user=obj.get_user_by_name(username))
        else:
            message = 'Neither of user_id and username are specified'
            logger.error(message)
            raise QueryParametersNotSpecified(message)

    return wrapped


def id_or_title(func):
    def wrapped(obj, vehicle_id=None, title=None):

        if vehicle_id is not None:
            return func(obj, vehicle=obj.get_vehicle_by_id(vehicle_id))
        elif title is not None:
            return func(obj, vehicle=obj.get_vehicle_by_title(title))
        else:
            message = 'Neither of vehicle_id and title are specified'
            logger.error(message)
            raise QueryParametersNotSpecified(message)

    return wrapped


class DBSteps(DBClient):

    def __init__(self, db_name, username, password, host='127.0.0.1', port='5432', autocomit=False, autoflush=False,
                 save_when_exit=False, log=False):

        super().__init__(db_name, username, password, db_type='postgresql', dbapi='psycopg2', host=host, port=port,
                         autocomit=autocomit, autoflush=autoflush, save_when_exit=save_when_exit, log=log)

    def get_user_by_name(self, username):
        return self.query(Users).filter(Users.name == username).first()

    def get_user_by_id(self, user_id):
        return self.query(Users).filter(Users.id == user_id).first()

    @id_or_name
    def get_user_login(self, user=None):
        return user.login

    @id_or_name
    def get_user_password(self, user=None):
        return user.password

    @id_or_name
    def get_user_vehicles(self, user=None):
        return user.vehicles

    def get_vehicle_by_title(self, title):
        return self.query(Vehicles).filter(Vehicles.title == title).first()

    def get_vehicle_by_id(self, vehicle_id):
        return self.query(Vehicles).filter(Vehicles.id == vehicle_id).first()

    @id_or_title
    def get_vehicle_type(self, vehicle=None):
        return vehicle.type

    @id_or_title
    def get_vehicle_price(self, vehicle=None):
        return vehicle.price

    @id_or_title
    def get_users_owing_vehicle(self, vehicle=None):
        return vehicle.users


class DBStepsException(Exception):
    pass


class QueryParametersNotSpecified(DBStepsException):
    pass
