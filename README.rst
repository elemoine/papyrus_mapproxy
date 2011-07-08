papyrus_mapproxy
=================

papyrus_mapproxy provides an easy and convenient method for embedding MapProxy
in Pyramid applications.

The source code of papyrus_mapproxy is straightforward, so if
papyrus_mapproxy doesn't do what you want, open its source code, get
inspiration, and write your own code.

Install
-------

papyrus_mapproxy can be installed with ``easy_install``::

    $ easy_install papyrus_mapproxy

Often you'll want to make papyrus_mapproxy a dependency of your Pyramid
application, which is done by adding ``papyrus_mapproxy`` to the
``install_requires`` list defined in the Pyramid application's ``setup.py``
file.

Embed MapProxy
---------------

Embedding MapProxy in a Pyramid application is easy.

Edit the application's ``development.ini`` file and, in the main section
(``[app:]``), set ``mapproxy.yaml`` to the location of the MapProxy config
file. Example::

    [app:MyApp]
    use = egg:MyApp
    ...
    mapproxy.yaml = %(here)s/mapproxy.yaml

In this example the MapProxy config file is located at the same location as the
``development.ini`` file. (As an example you can use this MapProxy config `file
<https://github.com/elemoine/papyrus_mapproxy/blob/master/mapproxy.yaml>`_.)

Now, edit the application's main file, ``__init__.py``, and register
papyrus_mapproxy using the ``Configurator.include`` method::

    def main(global_config, **settings):

        config = Configurator(settings=settings)

        import papyrus_mapproxy
        config.include(papyrus_mapproxy)

That's it! The Pyramid application now exposes a MapProxy service at
``/mapproxy``. Try http://localhost:6543/mapproxy/demo.
