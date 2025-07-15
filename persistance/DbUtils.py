from contextlib import contextmanager
from sqlalchemy import Table, MetaData, create_engine, select, insert

class DbUtils:
    engine = create_engine('mysql+mysqldb://root:password@localhost:3306/bank')

    @classmethod
    @contextmanager
    def db_query(cls, stmt):
        connection = cls.engine.connect()
        yield connection.execute(stmt)
        connection.commit()
        connection.close()



