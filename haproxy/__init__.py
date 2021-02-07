"""HAProxy Python library.

"""

# pylint: disable=bad-whitespace

__version__    = (1, 0, 0)
__versionstr__ = '.'.join(map(str, __version__))
__license__    = 'The MIT License (MIT)'
__copyright__  = 'Copyright (C) 2021 Dimitris Bliamplias'

from haproxy.haproxy_acl import HAProxyACL
