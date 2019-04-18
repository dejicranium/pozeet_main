from pyramid.config import Configurator


SETTINGS = None
def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    SETTINGS = settings
    config = Configurator(settings=settings,)
    config.include('pyramid_jinja2')
    config.include('.models')
    config.include('.cors')
    config.add_cors_preflight_handler()
    config.include('.routes')
    config.include('.security')
    config.include('..greggo')
    #config.add_static_view('repoll_static', path='repoll:repoll_static')
    config.add_static_view(name='https://s3.us-east-2.amazonaws.com/pozeet-static/', path='repoll:repoll_static')
    config.add_static_view(name='https://s3.us-east-2.amazonaws.com/pozeet-static/js', path='repoll:js')
    #config.add_static_view(name='static/js/repoll/dist', path="repoll:js")
    
    #config.add_static_view('repoll_static/js/repoll/dist',path='repoll:js')
    config.scan()
    return config.make_wsgi_app()
