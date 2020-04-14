from views import handle, post_handle

def setup_routes(app):
    app.router.add_get('/', handle)
    app.router.add_post('/post/', post_handle)
