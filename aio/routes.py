from .views import handle, users_list, user_detail, seesion_redis, invalidate_seesion_redis


def setup_routes(app):
    app.router.add_get('/', handle)
    app.router.add_get('/users/', users_list)
    app.router.add_get('/users/{id}/', user_detail)
    app.router.add_get('/login/', seesion_redis)
    app.router.add_get('/logout/', invalidate_seesion_redis)
