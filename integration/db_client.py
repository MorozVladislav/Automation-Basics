#!/usr/bin/env python3
# -*- coding: ascii -*-
import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


class DBClient(Session):

    def __init__(self, db_name, username, password, db_type='postgresql', dbapi='psycopg2', host='127.0.0.1',
                 port='5432', autocomit=False, autoflush=False, save_when_exit=False, log=False):

        self.db_type = db_type
        self.dbapi = dbapi
        self.host = host
        self.port = port
        self.db_name = db_name
        self.username = username
        self.password = password
        self._engine = create_engine('{}+{}://{}:{}@{}:{}/{}'.format(
            self.db_type,
            self.dbapi,
            self.username,
            self.password,
            self.host,
            self.port,
            self.db_name
        ), echo=log)

        super().__init__(bind=self._engine, autocommit=autocomit, autoflush=autoflush)
        self.save_when_exit = save_when_exit
        self._base = declarative_base(bind=self._engine)

    def __del__(self):
        if self.save_when_exit:
            self.save_all()
        self.close()
        logger.info('Session for {}@{}:{}/{} was closed'.format(
            self.username,
            self.host,
            self.port,
            self.db_name
        ))

    def save_all(self):
        self._base.metadata.create_all()
        self.commit()
        logger.info('All changes were saved')

    def create_tables(self, tables_list=None):
        if tables_list is None:
            self._base.metadata.create_all(bind=self._engine)
        else:
            tables = []
            for table in tables_list:
                tables.append(table.__table__)
            self._base.metadata.create_all(bind=self._engine, tables=tables)

    def delete_tables(self, tables_list=None):
        self.save_all()
        if tables_list is None:
            self._base.metadata.drop_all(bind=self._engine)
        else:
            tables = []
            for table in tables_list:
                tables.append(table.__table__)
            self._base.metadata.drop_all(bind=self._engine, tables=tables)
