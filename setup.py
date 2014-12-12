# coding: utf-8

import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.txt')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'pyramid',
    'pyramid_debugtoolbar',
    'pyramid_jinja2',
    'pyramid_tm',
    'pyramid_redis_sessions',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    'colander',
    'deform',
    'click',
    'werkzeug',
]

setup(name='potte',
      version='0.0',
      description='potte',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='potte',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = potte:main
      [console_scripts]
      potte = potte.scripts.potte:main
      """,
      )
