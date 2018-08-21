#!/usr/bin/env python3
# -*- coding: ascii -*-
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

association = Table('association', Base.metadata,
                    Column('user_id', Integer, ForeignKey('users.id')),
                    Column('vehicle_id', Integer, ForeignKey('vehicles.id')))


class Users(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    login = Column(String)
    password = Column(String)
    vehicles = relationship('Vehicles', secondary=association, back_populates='users')


class Vehicles(Base):

    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    type = Column(String)
    price = Column(Float)
    users = relationship('Users', secondary=association, back_populates='vehicles')
