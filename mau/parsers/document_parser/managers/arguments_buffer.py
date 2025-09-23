from __future__ import annotations

from mau.parsers.arguments_parser.parser import Arguments


class ArgumentsBuffer:
    def __init__(self):
        # This is there the manager keeps the
        # stored arguments.
        self._arguments: Arguments | None = None

    def push(self, arguments: Arguments):
        self._arguments = arguments

    def pop(self) -> Arguments | None:
        arguments = self._arguments
        self._arguments = None

        return arguments

    def pop_or_default(self) -> Arguments:
        return self.pop() or Arguments()
