import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

install_requires = [
    'pyramid',
    'WebError',
    'MapProxy'
    ]

setup_requires = [
    'nose'
    ]

tests_require = install_requires + [
    'coverage'
    ]

setup(name='papyrus_mapproxy',
      version='0.1',
      description='papyrus_mapproxy',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='Eric Lemoine',
      author_email='eric.lemoine@gmail.com',
      url='http://github.com/elemoine/papyrus_mapproxy',
      keywords='web geospatial papyrus mapproxy pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      setup_requires=setup_requires,
      tests_require=tests_require,
      test_suite="papyrus_mapproxy.tests",
      entry_points = """\
      [paste.app_factory]
      main = papyrus_mapproxy:main
      """,
      paster_plugins=['pyramid'],
      )
