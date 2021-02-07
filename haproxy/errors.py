"""Exception handling module for haproxy."""


class HAProxyGenericError(Exception):
    """Base exception for the haproxy module."""
    def __init__(self, msg):
        super(HAProxyGenericError, self).__init__()
        if isinstance(msg, list):
            msg = ' '.join(msg)
        self.message = msg

    def __str__(self):
        return self.message


class CommandExecError(HAProxyGenericError):
    """Exception denoting a failure during command execution."""
