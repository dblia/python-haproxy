#!/usr/bin/python3

"""Python setup configuration script."""

from os.path import join, dirname
from setuptools import setup, find_packages

from haproxy import __versionstr__ as version


def file_read(fname):
    """Utility function to read from the given file."""
    return open(join(dirname(__file__), fname)).read()

def get_classifiers():
    """Return package metadata information."""
    return [
        'Private :: Do Not Upload',
        'Development Status :: 4 - Beta',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: The MIT License (MIT)',
    ]

setup(
    name                = 'haproxy',
    version             = version,
    description         = 'HAProxy dynamic ACL configuration library',
    long_description    = file_read('README.rst'),
    keywords            = 'haproxy acl socket dynamic api python',
    classifiers         = get_classifiers(),

    author              = 'Dimitris Bliamplias',
    author_email        = 'bl.dimitris@gmail.com',
    maintainer          = 'Dimitris Bliamplias',
    maintainer_email    = 'bl.dimitris@gmail.com',
    license             = file_read('LICENSE'),
    url                 = 'https://github.com/dblia/python-haproxy',

    packages            = find_packages(exclude=('tests',)),
    install_requires    = [],
    platforms           = 'linux',

    include_package_data = True,
    zip_safe             = False,

    # declare scripts to be available to our PATH
    scripts              = [],
)
