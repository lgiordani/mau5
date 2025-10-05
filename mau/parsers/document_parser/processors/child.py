from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .parser import DocumentParser


from mau.text_buffer.context import Context
from mau.tokens.token import TokenType


def child_processor(parser: DocumentParser):
    # Parse child text in the form
    #
    # . This is a title
    # or
    # .role This is a title
    #
    # The default role is "title".

    # Parse the mandatory dot
    prefix = parser.tm.get_token(
        TokenType.TITLE, value_check_function=lambda x: x.startswith(".")
    )

    role = prefix.value[1:] or "title"

    # Get the text of the title
    text = parser.tm.get_token(TokenType.TEXT)

    parser.children_buffer.push(role, text.value, text.context, parser.environment)

    return True
