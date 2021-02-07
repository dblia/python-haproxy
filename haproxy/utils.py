"""Utility functions for the haproxy module."""


def cmd_succeeded(output, ignored_outputs=None):
    """Check if the given output contains an error.

    Most commonly a succeeded command will return an empty string. However, some
    commands even though have succeeded return an informative message to the
    caller. This helper function checks the status of a given output and if it's
    empty or the message is included in the ignored_outputs list, it marks the
    command status as successful.

    @param output (list): the output of the command
    @param ignored_outputs (list): list of known output strings to be ignored

    @return (bool): True if the command succeeded, False otherwise

    """
    if ignored_outputs is None:
        ignored_outputs = []

    if output and output[0] not in ignored_outputs:
        return False
    return True
