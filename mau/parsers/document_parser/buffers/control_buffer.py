from __future__ import annotations

from enum import Enum

from mau.environment.environment import Environment
from mau.parsers.base_parser.parser import MauParserException
from mau.text_buffer.context import Context


class ControlComparisons(Enum):
    EQUAL_EQUAL = "=="
    BANG_EQUAL = "!="


class Control:
    def __init__(
        self,
        operator: str,
        variable: str,
        comparison: str,
        value: str,
        context: Context | None = None,
    ):
        if operator not in ["if"]:
            raise MauParserException(
                f"Control operator '{operator}' is not supported.",
                context,
            )

        self.operator = operator
        self.variable = variable
        self.comparison = ControlComparisons(comparison)
        self.value = value
        self.context = context

    def process(self, environment: Environment) -> bool:
        variable_value = environment.getvar(self.variable)

        match self.comparison:
            case ControlComparisons.EQUAL_EQUAL:
                return variable_value == self.value
            case ControlComparisons.BANG_EQUAL:
                return variable_value != self.value


class ControlBuffer:
    def __init__(self):
        # This is where the manager keeps the
        # stored control instructions.
        self._control: Control | None = None

    def push(self, control: Control):
        self._control = control

    def pop(self):
        control = self._control
        self._control = None

        return control
