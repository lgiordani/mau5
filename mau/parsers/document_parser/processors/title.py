from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .parser import DocumentParser


from mau.tokens.token import TokenType


def title_processor(parser: DocumentParser):
    # Parse a title in the form
    #
    # . This is a title
    # or
    # .This is a title

    # Parse the mandatory dot
    dot = parser.tm.get_token(TokenType.TITLE, ".")

    # Get the text of the title
    text = parser.tm.get_token(TokenType.TEXT).value
    parser.tm.get_token(TokenType.EOL)

    parser.title_manager.push(text, dot.context, parser.environment)

    return True
