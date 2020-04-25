from .views import handle, users_list, user_detail, seesion_redis, invalidate_seesion_redis, jwt_login, test


def setup_routes(app):
    app.router.add_get('/', handle)
    app.router.add_get('/users/', users_list)
    app.router.add_get('/users/{id}/', user_detail)
    app.router.add_post('/session_login/', seesion_redis)
    app.router.add_get('/session_logout/', invalidate_seesion_redis)
    app.router.add_post('/jwt_login/', jwt_login)
    app.router.add_get('/test/', test)
