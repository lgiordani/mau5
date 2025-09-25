from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .parser import DocumentParser


from mau.parsers.document_parser.buffers.control_buffer import Control
from mau.tokens.token import TokenType


def control_processor(parser: DocumentParser):
    # Parse control instructions in the form
    #
    # @OPERATOR VARIABLE COMPARISON VALUE

    # Parse the mandatory @
    prefix = parser.tm.get_token(TokenType.CONTROL, "@")

    # Get the operator
    operator = parser.tm.get_token(TokenType.TEXT).value

    # Get the variable
    variable = parser.tm.get_token(TokenType.TEXT).value

    # Get the comparison
    comparison = parser.tm.get_token(TokenType.TEXT).value

    # Get the value
    value = parser.tm.get_token(TokenType.TEXT).value

    control = Control(operator, variable, comparison, value, prefix.context)
    parser.control_buffer.push(control)

    return True
