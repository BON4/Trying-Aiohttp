from aiohttp import web
import json
from db import db_model
import datetime
from aiohttp_session import get_session
import time
from .auth_backend import is_authenticated_cookie
from datetime import datetime, timedelta
from sqlalchemy.sql import text
import jwt
from settings import JWT_SECRET, JWT_ALGORITHM, JWT_EXP_DELTA_SECONDS

print(__name__)


async def test(request):

    return web.Response(text=json.dumps(request.user))


async def jwt_login(request):
    post = await request.post()
    try:
        async with request.app['db'].acquire() as conn:
            cursor = await conn.execute(text("SELECT * FROM users WHERE users.email = :email and users.password = :password"), {'email': post['email'], 'password': post['password']})
            records = await cursor.fetchall()
            users = [dict(u) for u in records]
            if(len(users) == 0):
                raise web.HTTPBadRequest()
            for record in users:
                record['date'] = record['date'].strftime("%m/%d/%Y")
    except KeyError:
        raise web.HTTPBadRequest()

    payload = {
        'id': record['id'],
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
    }
    jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
    return web.json_response({'token': jwt_token.decode('utf-8')})


async def seesion_redis(request):
    post = await request.post()

    session = await get_session(request)
    session['last_visit'] = time.asctime()
    print(session.identity, request.get("aiohttp_session"))
    return web.Response(text=f"Your last visit: {session['last_visit']}")


@is_authenticated_cookie
async def invalidate_seesion_redis(request):
    session = await get_session(request)
    last_visit = session['last_visit'] if 'last_visit' in session else None
    if(last_visit != None):
        session.invalidate()
    return web.Response(text=f"Your session have been invalidated")


@is_authenticated_cookie
async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


@is_authenticated_cookie
async def users_list(request):
    try:
        async with request.app['db'].acquire() as conn:
            cursor = await conn.execute(db_model.user.select())
            records = await cursor.fetchall()
            users = [dict(u) for u in records]
            for record in users:
                record['date'] = record['date'].strftime("%m/%d/%Y")
    except json.JSONDecodeError as e:
        return web.HTTPBadRequest()

    return web.Response(text=json.dumps(users))


@is_authenticated_cookie
async def user_detail(request):
    user_id = request.match_info.get('id', None)
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(db_model.user.select().where(db_model.user.c.id == user_id))
        records = await cursor.fetchall()
        users = [dict(u) for u in records]
        for record in users:
            record['date'] = record['date'].strftime("%m/%d/%Y")
    return web.Response(text=json.dumps(users))
