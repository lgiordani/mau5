from __future__ import annotations

from mau.parsers.arguments_parser import Arguments


class ArgumentsBuffer:
    """This is a buffer for arguments
    collected in the source text."""

    def __init__(self):
        # This is where the buffer keeps the
        # stored arguments.
        self._arguments: Arguments | None = None

    def push(self, arguments: Arguments):
        # Store the given arguements.
        self._arguments = arguments

    def pop(self) -> Arguments | None:
        # Retrieve the stored arguments
        # and reset the internal slot.
        arguments = self._arguments
        self._arguments = None

        return arguments

    def pop_or_default(self) -> Arguments:
        # Retrieve the stored arguments
        # and reset the internal slot.
        # Return an empty Arguments object
        # if nothing is stored.
        return self.pop() or Arguments()
