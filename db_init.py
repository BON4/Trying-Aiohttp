from sqlalchemy import create_engine, MetaData
import datetime
from db.db_model import user
from settings import config

DSN = "postgresql://vlad:1488@localhost:5432/try_aio"


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[user])


def sample_data(engine):
    conn = engine.connect()
    conn.execute(user.insert(), [
        {
            'username': 'test3',
            'email': 'test3@gmail.com',
            'password': '1488',
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'is_stuff': 0
        }
    ])
    conn.close()


if __name__ == '__main__':
    db_url = DSN.format(**config['postgres'])
    engine = create_engine(db_url)

    create_tables(engine)
    sample_data(engine)
