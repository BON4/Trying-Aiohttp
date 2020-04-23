import aiohttp_jinja2
from aiohttp import web
import aioredis
import asyncio
import aiohttp_session
from aiohttp_session.redis_storage import RedisStorage


async def make_redis_pool():
    redis_address = ('localhost', '6379')
    return await aioredis.create_pool(
        redis_address,
        create_connection_timeout=1,
    )


async def handle_404(request):
    return aiohttp_jinja2.render_template('404.html', request, {})


async def handle_401(request):
    return aiohttp_jinja2.render_template('401.html', request, {})


async def handle_500(request):
    return aiohttp_jinja2.render_template('500.html', request, {})


def create_error_middleware(overrides):

    @web.middleware
    async def error_middleware(request, handler):
        try:
            response = await handler(request)

            override = overrides.get(response.status)
            if override:
                return await override(request)

            return response

        except web.HTTPException as ex:
            override = overrides.get(ex.status)
            if override:
                return await override(request)

            raise

    return error_middleware


def setup_middlewares(app):
    loop = asyncio.get_event_loop()
    redis_pool = loop.run_until_complete(make_redis_pool())
    storage = RedisStorage(redis_pool)
    session_middleware = aiohttp_session.session_middleware(storage)

    error_middleware = create_error_middleware({
        401: handle_401,
        404: handle_404,
        500: handle_500
    })
    app.middlewares.append(error_middleware)
    app.middlewares.append(session_middleware)
