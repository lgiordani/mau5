from __future__ import annotations

from enum import Enum

from mau.environment.environment import Environment
from mau.lexers.control_lexer.lexer import ControlLexer
from mau.parsers.base_parser.parser import BaseParser, MauParserException
from mau.text_buffer.context import Context
from mau.tokens.token import Token, TokenType


class ControlOperators(Enum):
    EQUAL_EQUAL = "=="
    BANG_EQUAL = "!="


class Control:
    def __init__(
        self,
        variable: str,
        operator: ControlOperators,
        value: str,
        context: Context | None = None,
    ):
        if operator not in ["if", "true", "false"]:
            raise MauParserException(
                f"Control operator '{operator}' is not supported.",
                context,
            )

        # self.operator = operator
        # self.logic = logic
        # self.context = context
        pass

    def process(self) -> bool:
        # match self.operator:
        #     case "true":
        #         return True
        #     case _:
        #         return False
        return True

    #     try:
    #         variable, test = statement.split(":", 1)
    #     except ValueError:
    #         self._error(f"Statement '{statement}' is not in the form variable:test")

    #     variable_value = self.environment.getvar(variable, None)

    #     if variable_value is None:
    #         self._error(f"Variable '{variable}' has not been defined")

    #     if test.startswith("="):
    #         value = test[1:]
    #         return variable_value == value

    #     if test.startswith("!="):
    #         value = test[2:]

    #         return variable_value != value

    #     if test.startswith("&"):
    #         value = test[1:]

    #         if value not in ["true", "false"]:
    #             self._error(f"Boolean value '{value}' is invalid")

    #         # pylint: disable=simplifiable-if-expression
    #         value = True if value == "true" else False

    #         return variable_value and value

    #     self._error(f"Test '{test}' is not supported")

    # def _reset_control(self):
    #     self.control = (None, None, None)


class ControlParser(BaseParser):
    lexer_class = ControlLexer

    def __init__(
        self,
        tokens: list[Token],
        environment: Environment | None = None,
        parent_node=None,
        parent_position=None,
    ):
        super().__init__(tokens, environment, parent_node, parent_position)

        self.control: Control | None = None

    def _process_functions(self):
        return [
            self._process_eol,
            self._process_control,
        ]

    def _process_eol(self):
        # This simply ignores the end of line.

        self.tm.get_token(TokenType.EOL)

        return True

    def _process_control(self):
        variable_token = self.tm.get_token(TokenType.TEXT)
        operator_token = self.tm.get_token(TokenType.TEXT)
        value_token = self.tm.get_token(TokenType.TEXT)

        self.control = Control(
            variable=variable_token.value,
            operator=operator_token.value,
            value=value_token.value,
            context=variable_token.context,
        )

        return True
