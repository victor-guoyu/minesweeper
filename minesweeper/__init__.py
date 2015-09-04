from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('cornice')
    config.add_route('index', '/')
    config.add_route('assets', '/assets/*subpath')
    config.add_view('minesweeper.static.index_static_view', route_name='index')
    config.add_view('minesweeper.static.assets_static_view', route_name='assets')
    config.scan('minesweeper.controllers')
    return config.make_wsgi_app()
