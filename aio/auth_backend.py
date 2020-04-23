from aiohttp_session import get_session
from aiohttp import web


def is_authenticated_cookie(f):
    async def wrapper_arg(request):
        session = await get_session(request)
        try:
            last_visit = session['last_visit']
            return await f(request)
        except KeyError:
            raise web.HTTPUnauthorized()
    return wrapper_arg
