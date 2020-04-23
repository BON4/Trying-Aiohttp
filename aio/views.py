from aiohttp import web
import json
from db import db_model
import datetime
from aiohttp_session import get_session
import time
from .auth_backend import *

print(__name__)


async def seesion_redis(request):
    session = await get_session(request)
    last_visit = session['last_visit'] if 'last_visit' in session else None
    session['last_visit'] = time.asctime()
    print(session.identity, request.get("aiohttp_session"))
    return web.Response(text=f"Your last visit: {last_visit}")


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
