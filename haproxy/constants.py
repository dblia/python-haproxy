"""Constants and helper definitions."""

# pylint: disable=bad-whitespace

import os


def _env_get(name, default=None):
    """Get the value of the given env variable name."""
    return os.environ.get("{}{}".format("HA_", name), default)

def _set_bool(val):
    """Helper to convert the given value to boolean."""
    true_values = ['true', 'yes', 'y', 'on', '1']
    return isinstance(val, str) and val.lower() in true_values


HA_SOCK_FILE    = _env_get('SOCK_FILE', "/run/haproxy/admin.sock")
HA_SOCK_TIMEOUT = float(_env_get('SOCK_TIMEOUT', 0.2))
HA_DEBUG        = _set_bool(_env_get('DEBUG', False))
