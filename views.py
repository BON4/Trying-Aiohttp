from aiohttp import web
import json

async def handle(request):
    print(request)
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

async def post_handle(request):
    try:
        post = await request.json()
        print(post['email'], post['password'], sep='\n')
    except json.JSONDecodeError as e:
        return web.HTTPBadRequest()

    return web.Response(text="exemple")
