import aiopg.sa
from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, Date, Boolean
)

meta = MetaData()

user = Table(
    'users',
    meta,
    Column('id', Integer, primary_key=True),
    Column('username', String(100), nullable=False),
    Column('email', String, nullable=False),
    Column('password', String(100), nullable=False),
    Column('date', Date, nullable=False),
    Column('is_stuff', Boolean, nullable=False)
)


async def init_pg(app):
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
    )
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()
