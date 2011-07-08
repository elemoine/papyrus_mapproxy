from pyramid.config import Configurator
from pyramid.wsgi import wsgiapp2, wsgiapp

from mapproxy.config.loader import load_configuration, ConfigurationError
from mapproxy.wsgiapp import MapProxyApp

import logging
log = logging.getLogger('papyrus_mapproxy')

def load_mapproxy_config(mapproxy_config_file):
    try:
        mapproxy_config = load_configuration(mapproxy_conf=mapproxy_config_file)
    except ConfigurationError, e:
        log.fatal(e)
        raise
    return mapproxy_config

def create_view_callable(mapproxy_config):
    app = MapProxyApp(mapproxy_config.configured_services(),
                      mapproxy_config.base_config)
    return wsgiapp2(app.__call__)

def add_route(config, view):
    config.add_route('mapproxy', '/mapproxy/*subpath')
    config.add_view(view=view, route_name='mapproxy')

def includeme(config):
    """ The callable making it possible to include papyrus_mapproxy
    in a Pyramid application.

    Calling ``config.include(papyrus_mapproxy)`` will result in this
    callable being called.

    Arguments:

    * ``config``: the ``pyramid.config.Configurator`` object.
    """
    settings = config.get_settings()
    mapproxy_config = load_mapproxy_config(settings.get('mapproxy.yaml'))
    view = create_view_callable(mapproxy_config)
    add_route(config, view)


def main(global_config, **settings):
    """ Return the Pyramid application.
    """
    config = Configurator(settings=settings)
    config.include(includeme)
    return config.make_wsgi_app()


