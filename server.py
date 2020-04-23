from aiohttp import web
from aio.routes import setup_routes
from settings import config, BASE_DIR
from db.db_model import close_pg, init_pg
from aio.middlewares import setup_middlewares
import aiohttp_jinja2
import jinja2

print(str(BASE_DIR / 'try_aio' / 'templates'))

app = web.Application()
setup_middlewares(app)
app['config'] = config
aiohttp_jinja2.setup(app,
                     loader=jinja2.FileSystemLoader(str(BASE_DIR / 'try_aio' / 'templates')))
setup_routes(app)

# Start db signal
app.on_startup.append(init_pg)
# Sutdown db signal
app.on_cleanup.append(close_pg)

web.run_app(app)
