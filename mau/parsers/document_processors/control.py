from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mau.parsers.document_parser import DocumentParser


from mau.parsers.buffers.control_buffer import Control
from mau.text_buffer import Context
from mau.token import TokenType
from mau.parsers.condition_parser import ConditionParser


def control_processor(parser: DocumentParser):
    # Parse control instructions in the form
    #
    # @OPERATOR CONDITION

    # Parse the mandatory @
    prefix_token = parser.tm.get_token(TokenType.CONTROL, "@")

    # Get the operator
    operator = parser.tm.get_token(TokenType.TEXT).value

    # Get the condition
    condition_token = parser.tm.get_token(TokenType.TEXT)

    # Unpack the text initial position.
    start_line, start_column = condition_token.context.start_position

    # Get the text source.
    source_filename = condition_token.context.source

    # Replace variables
    condition_parser = ConditionParser.lex_and_parse(
        text=condition_token.value,
        message_handler=parser.message_handler,
        environment=parser.environment,
        start_line=start_line,
        start_column=start_column,
        source_filename=source_filename,
    )

    # At the moment we support only one condition.
    condition_node = condition_parser.condition_node

    # Find the final context.
    context = Context.merge_contexts(prefix_token.context, condition_token.context)

    control = Control(
        operator,
        condition_node.variable,
        condition_node.comparison,
        condition_node.value,
        context,
    )

    parser.control_buffer.push(control)

    return True
