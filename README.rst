.. _readme:

================
 Python HAProxy
================

.. contents:: **Contents Table**

*python-haproxy* is a *tiny* library to dynamically interact with a subset of the HAProxy's Runtime
API.

Overview
========

`HAProxy`_ is well-known software written in C for providing fast and efficient load balancing for
TCP and HTTP-based applications with the ability to spread requests across multiple servers. Via
its `Runtime API`_ (previously known as HAProxy *stats socket*) you have the ability to run
commands against HAProxy's ACLs, stick tables, TLS ticket keys, etc with the benefit that those
commands would take effect immediately. You can also retrieve real-time statistics, enable/disable
frontends or affect backend server's weights, making this API a very powerful and useful HAProxy
feature.

The creation of this *tiny* Python library was driven by the need to update HAProxy's ACLS during
runtime and this is the only supported feature from the Runtime API at the moment.

.. _HAProxy:
   https://www.haproxy.com
.. _Runtime API:
   https://www.haproxy.com/blog/dynamic-configuration-haproxy-runtime-api

Requirements
============

You don't need any special requirements in order to run the current tool. Just a working *Python3*
environment and the HAProxy's Runtime API enabled. You can enabled the Runtime API by following the
next example:

::

    global
        stats socket /run/haproxy/admin.sock mode 660 level admin
        stats timeout 2m

**NOTE**: The current library has been mostly used by single process HAProxy setups between
versions **1.8+** to **2.0+** and Python versions **3.5** to **3.7**.

Installation guide
==================

* To install the package from the source:

::

    # clone the ``python-haproxy`` repository:
    #
    $ git clone git@github.com:dblia/python-haproxy.git

    # and install it using the python `setuptools`_ libary:
    #
    $ python3 setup.py build
    $ sudo python3 setup.py install

.. _setuptools: https://setuptools.readthedocs.io/en/latest/

Getting Started
===============

- Quickly identify the library's version:

::

   $ python -c 'import haproxy; print(haproxy.__versionstr__)'
   1.0.0

- How to use it

.. code-block:: python

    >>> import haproxy
    >>> haproxy.__versionstr__
    '1.0.0'
    >>>
    >>> from haproxy import HAProxyACL
    >>> ha = HAProxyACL('/etc/haproxy/whitelisted')
    >>> ha.add('8.8.8.8')
    True
    >>> ha.add('1.1.1.1')
    True
    >>> ha.update('8.8.8.8')
    True
    >>> ha.show()
    ['0x7f4cb0027360 8.8.8.8', '0x7f4ca402b330 1.1.1.1']
    >>> ha.delete('1.1.1.1')
    True
    >>> ha.show()
    ['0x7f4cb0027360 8.8.8.8']



.. vim: set textwidth=99 :
.. Local Variables:
.. mode: rst
.. fill-column: 99
.. End:
