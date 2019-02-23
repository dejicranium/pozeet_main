from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

<<<<<<< HEAD
import os
from wsgiref.simple_server import make_server
from paste.deploy import loadapp

here = os.path.abspath(os.path.dirname(__file__))


def get_app():
    return loadapp('config:%s/production.ini' % here)

app = get_app()

if __name__ == '__main__':
    server = make_server('0.0.0.0', 8888, app)
    server.serve_forever()
=======
def hello_world(request):
    return Response('Hello %(name)s!' % request.matchdict)

def generate_wsgi_app(app, environ):
    config = Configurator()
    config.add_route('hello', '/hello/{name}')
    config.add_view(hello_world, route_name='hello')
    wsgi_app = config.make_wsgi_app()
    return wsgi_app(app, environ)
>>>>>>> 983e7c36572509d54a03577a1df1f4fba1e4c334
