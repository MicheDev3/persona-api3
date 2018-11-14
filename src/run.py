from waitress import serve

from src import *
from src.api.v1 import *
from src.middleware import *

app = falcon.API(
    middleware=middleware
)

app.add_route('/api/v1/people', People())
app.add_route('/api/v1/search', Search())

app.add_error_handler(Exception, custom_error_handler)

if __name__ == '__main__':
    serve(app, host=settings.HOST, port=settings.PORT, url_scheme='https')
