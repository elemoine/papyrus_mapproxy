import os
import unittest

class LoadMapProxyConfigTests(unittest.TestCase):
    def test_success(self):
        from papyrus_mapproxy import load_mapproxy_config
        from mapproxy.config.loader import ProxyConfiguration
        curdir = os.path.dirname(os.path.abspath(__file__))
        cfgfile = os.path.join(curdir, 'mapproxy.yaml')
        conf = load_mapproxy_config(cfgfile)
        self.assertTrue(isinstance(conf, ProxyConfiguration))

    def test_failure(self):
        from papyrus_mapproxy import load_mapproxy_config
        from mapproxy.config.loader import ConfigurationError
        curdir = os.path.dirname(os.path.abspath(__file__))
        cfgfile = os.path.join(curdir, 'mapproxy_bad.yaml')
        self.assertRaises(ConfigurationError, load_mapproxy_config, cfgfile)

class AddRouteTests(unittest.TestCase):

    # _makeOne, _getViewCallable, and _getRouteRequestIface come from Pyramid
    # pyramid/tests/test_config.py:ConfiguratorTests

    def _makeOne(self, *arg, **kw):
        from pyramid.config import Configurator
        return Configurator(*arg, **kw)

    def _getViewCallable(self, config, ctx_iface=None, request_iface=None,
                         name='', exception_view=False):
        from zope.interface import Interface
        from pyramid.interfaces import IRequest
        from pyramid.interfaces import IView
        from pyramid.interfaces import IViewClassifier
        from pyramid.interfaces import IExceptionViewClassifier
        if exception_view:
            classifier = IExceptionViewClassifier
        else:
            classifier = IViewClassifier
        if ctx_iface is None:
            ctx_iface = Interface
        if request_iface is None:
            request_iface = IRequest
        return config.registry.adapters.lookup(
            (classifier, request_iface, ctx_iface), IView, name=name,
            default=None)

    def _getRouteRequestIface(self, config, name):
        from pyramid.interfaces import IRouteRequest
        iface = config.registry.getUtility(IRouteRequest, name)
        return iface

    def test(self):
        from pyramid.interfaces import IRoutesMapper
        from papyrus_mapproxy import add_route
        config = self._makeOne(autocommit=True)
        view = lambda *arg: "OK"
        add_route(config, view)
        mapper = config.registry.getUtility(IRoutesMapper)
        routes = mapper.get_routes()
        self.assertEqual(len(routes), 1)
        self.assertEqual(routes[0].name, 'mapproxy')
        self.assertEqual(routes[0].pattern, '/mapproxy/*subpath')
        request_iface = self._getRouteRequestIface(config, 'mapproxy')
        self.assertNotEqual(request_iface, None)
        wrapper = self._getViewCallable(config, request_iface=request_iface)
        self.assertEqual(wrapper, view)

from pyramid import testing

class IncludeMeTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        curdir = os.path.dirname(os.path.abspath(__file__))
        cfgfile = os.path.join(curdir, 'mapproxy.yaml')
        self.config.get_settings().update({'mapproxy.yaml': cfgfile})

    def tearDown(self):
        testing.tearDown()

    def test(self):
        from pyramid.interfaces import IRoutesMapper
        from papyrus_mapproxy import includeme
        includeme(self.config)
        mapper = self.config.registry.getUtility(IRoutesMapper)
        routes = mapper.get_routes()
        self.assertEqual(len(routes), 1)

class MainTests(unittest.TestCase):
    def test(self):
        from papyrus_mapproxy import main
        curdir = os.path.dirname(os.path.abspath(__file__))
        cfgfile = os.path.join(curdir, 'mapproxy.yaml')
        settings = {'mapproxy.yaml': cfgfile}
        app = main({}, **settings)
        from pyramid.router import Router
        self.assertTrue(isinstance(app, Router))

class MapProxyTests(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        curdir = os.path.dirname(os.path.abspath(__file__))
        cfgfile = os.path.join(curdir, 'mapproxy.yaml')
        self.config.get_settings().update({'mapproxy.yaml': cfgfile})

    def tearDown(self):
        testing.tearDown()

    def test_mapproxy(self):
        from pyramid.request import Request
        from papyrus_mapproxy import (load_mapproxy_config, create_view_callable,
                                      add_route)

        mapproxy_config_file = self.config.get_settings().get('mapproxy.yaml')
        mapproxy_config = load_mapproxy_config(mapproxy_config_file)

        view = create_view_callable(mapproxy_config)
        
        add_route(self.config, view)

        context = DummyContext()
        request = Request({'wsgi.url_scheme': 'http', 'SERVER_NAME': 'foo',
                           'SERVER_PORT': '80'})
        request.method = 'GET'
        response = view(context, request)
        from pyramid.response import Response
        self.assertTrue(isinstance(response, Response))
        self.assertTrue('Welcome to MapProxy' in response.body)

class DummyContext:
    pass
