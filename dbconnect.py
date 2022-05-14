""" Provides a DBSession class, for returning a alchemy session object
    The actual database connection will be done when the query is executed
"""

import sqlalchemy
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager


class DBSession:
    _engine = None
    _dsn = None

    @classmethod
    def initdsn(cls, dsn):
        cls._dsn = dsn

    @classmethod
    def get_session(cls):
        """ This is a class method. It will create the alchemy engine if it does not exist.
            Will return a new session object to be used to create a query
        """

        if cls._dsn is None:
            return None

        cls._engine = sqlalchemy.create_engine(
            f"mysql+mysqldb://{cls._dsn}", echo=False, pool_recycle=60)
        cls._Session = sessionmaker(bind=cls._engine)

        return cls._Session()


@contextmanager
def session_scope():
    connection = "root:qwerty123456@localhost/new?charset=utf8"
    dsn = connection
    DBSession.initdsn(dsn)
    session = DBSession.get_session()

    try:
        yield session
    finally:
        if session is not None:
            session.close()