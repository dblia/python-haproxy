"""A python library to dynamically configure HAProxy ACLs over the UNIX admin socket."""

import re
import socket
import sys

from haproxy.constants import HA_SOCK_FILE, HA_SOCK_TIMEOUT, HA_DEBUG
from haproxy.errors import CommandExecError
from haproxy.utils import cmd_succeeded

# pylint: disable=bad-whitespace


class HAProxyACL:
    """A class to dynamically configure HAProxy ACLs via the UNIX socket interface.

    """
    MATCH_RE    = re.compile(r'.*match=(?P<found>(yes|no))(,|.*)')

    KEY_MISSING = "Key not found."
    UNKNOWN_ACL = "Unknown ACL identifier. Please use #<id> or <file>."

    def __init__(self, acl_file, s_file=HA_SOCK_FILE, s_timeout=HA_SOCK_TIMEOUT, verbose=HA_DEBUG):
        """Initializes a HAProxyACL object.

        """
        self.acl_file       = acl_file
        self.socket_file    = s_file
        self.socket_timeout = s_timeout
        self.verbose        = verbose

        self._acl_exists()

    def _send(self, command):
        """Send the given command to HAProxy over the UNIX admin socket.

        This a helper that sends a command to HAProxy over the Unix admin
        socket interface. It splits the command's output on a newline and
        returns it as a list of strings.

        Note that HAProxy always includes an empty string at the end of its
        responses. So, we chose to remove it before we return the response to
        the caller, as it adds redundant noise to the output.

        @param command (str): the command to execute

        @return (list): the command's output as a list of strings

        """
        try:
            unix_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            unix_socket.settimeout(self.socket_timeout)
            unix_socket.connect(self.socket_file)
            if self.verbose:
                print("[DEBUG] RunCmd:", command)
            unix_socket.send((command + "\n").encode())

            file_handler = unix_socket.makefile()
            rdata = file_handler.read().splitlines()
        finally:
            unix_socket.close()

        return rdata[:-1]

    def _acl_exists(self):
        """Checks if the given ACL file exists.

        @raise CommandExecError: if the command execution failed
        @rtype (bool): True if the command execution succeeded

        """
        res = self._send("show acl {acl_f}".format(acl_f=self.acl_file))
        if not cmd_succeeded(res):
            raise CommandExecError(res)
        return True

    def add(self, data):
        """Adds an entry to the ACL.

        @raise CommandExecError: if the command execution failed
        @rtype (bool): True if the command execution succeeded

        """
        res = self._send("add acl {acl_f} {entry}".format(acl_f=self.acl_file, entry=data))
        if not cmd_succeeded(res):
            raise CommandExecError(res)
        return True

    def update(self, data):
        """Adds the given entry to the ACL only if it is missing."""
        if not self.entry_exists(data):
            return self.add(data)
        return True

    def delete(self, data):
        """Deletes the given ACL entry.

        @raise CommandExecError: if the command execution failed
        @rtype (bool): True if the command execution succeeded

        """
        res = self._send("del acl {acl_f} {entry}".format(acl_f=self.acl_file, entry=data))
        if not cmd_succeeded(res, ignored_outputs=[self.KEY_MISSING]):
            raise CommandExecError(res)
        return True

    def show(self):
        """Dumps the ACL's contents.

        @rtype (list): a list with the ACL's contents

        """
        return self._send("show acl {acl_f}".format(acl_f=self.acl_file))

    def clear_acl(self):
        """Clears the contents of the ACL.

        @raise CommandExecError: if the command execution failed
        @rtype (bool): True if the command execution succeeded

        """
        res = self._send("clear acl {acl_f}".format(acl_f=self.acl_file))
        if not cmd_succeeded(res):
            raise CommandExecError(res)
        return True

    def entry_exists(self, data):
        """Checks if the given entry exists in the ACL.

        Possible outputs of the `get acl` command are the following:

        * ['type=ip, case=sensitive, match=no']
        * ['type=ip, case=sensitive, match=yes, idx=tree, pattern="1.2.3.4"']

        In order to decide whether the given entry exists in the ACL, we first retrieve the value
        of the `match` key of the returned string via the `MATCH_RE` regex; then we simply check if
        it is set to `yes`.

        @rtype (bool): True if exists, False otherwise

        """
        command = "get acl {acl_f} {entry}".format(acl_f=self.acl_file, entry=data)
        res = self._send(command)[0]
        try:
            return self.MATCH_RE.search(res).groupdict()["found"] == "yes"
        except (IndexError, AttributeError, TypeError):
            return False
