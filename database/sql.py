

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

CONNECTION_STR = "mysql+pymysql://lcp:admin@localhost/binance?charset=utf8mb4"
DATABASE_NAME = "binance"
engines = {}


class DBAccess:

    def __init__(self, engine):
        self.connection = None
        self.session = None
        self.engine = engine
        self.create_session()

    def __del__(self):

        self.close()

    def __enter__(self):

        return self

    def __exit__(self, exception_type, exception_value, traceback):

        self.close()

    @staticmethod
    def get_db_instance():

        global engines

        db_name = DATABASE_NAME
        if db_name in engines:
            engine = engines[db_name]
        else:
            engine = create_engine(CONNECTION_STR,
                                   pool_size=0,
                                   echo=False)
            engines[db_name] = engine

        return DBAccess(engine)

    def close(self):
        if self.session is not None:
            self.session.close()
            self.session = None
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def begin(self):
        self.session.begin()

    def rollback(self):
        self.session.rollback()

    def commit(self):
        self.session.commit()

    def create_session(self):
            self.connection = self.engine.connect()
            session_class = sessionmaker(bind=self.connection, autocommit=True)
            self.session = session_class()