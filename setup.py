# -*- coding: utf-8 -*-
import os

from setuptools import setup
from setuptools import find_packages

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

with open(os.path.join(os.path.dirname(__file__), 'VERSION')) as f:
    VERSION = f.read().strip()

tests_require = ['django-storages', 'model-bakery',
                 'faker', 'django_environ', "django_webtest"]
# with open(os.path.join(os.path.dirname(__file__), 'requirements', f'trunk.txt')) as f:
#     for line in f:
#         tests_require.append(line.strip())

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='ambition-edc',
    version=VERSION,
    author=u'Erik van Widenfelt',
    author_email='ew2789@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/ambition-trial/ambition-edc',
    license='GPL license, see LICENSE',
    description='Ambition Trial EDC (https://doi.org/10.1186/ISRCTN72509687)',
    long_description=README,
    zip_safe=False,
    keywords='django ambition EDC',
    install_requires=[
        'boto3',
        'django==2.2.9',
        'django-environ',
        'django-redis',
        'django-storages',
        'celery',
        'django-celery-beat',
        'django-celery-results',
        'gunicorn',
        'python-memcached',
        'pyrabbit',
        'sentry_sdk',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    python_requires=">=3.7",
    tests_require=tests_require,
    test_suite='runtests.main',
)
