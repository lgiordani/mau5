from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .parser import DocumentParser


from mau.text_buffer.context import Context
from mau.parsers.document_parser.buffers.control_buffer import Control
from mau.tokens.token import TokenType


def control_processor(parser: DocumentParser):
    # Parse control instructions in the form
    #
    # @OPERATOR VARIABLE COMPARISON VALUE

    # Parse the mandatory @
    prefix_token = parser.tm.get_token(TokenType.CONTROL, "@")

    # Get the operator
    operator = parser.tm.get_token(TokenType.TEXT).value

    # Get the variable
    variable = parser.tm.get_token(TokenType.TEXT).value

    # Get the comparison
    comparison = parser.tm.get_token(TokenType.TEXT).value

    # Get the value
    value_token = parser.tm.get_token(TokenType.TEXT)

    # Find the final context.
    context = Context.merge_contexts(prefix_token.context, value_token.context)

    control = Control(operator, variable, comparison, value_token.value, context)
    parser.control_buffer.push(control)

    return True
