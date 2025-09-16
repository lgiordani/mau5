from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .parser import DocumentParser


from mau.parsers.base_parser.managers.tokens_manager import TokenError
from mau.parsers.base_parser.parser import MauParserException
from mau.tokens.token import Token, TokenType


def single_line_comment_processor(parser: DocumentParser):
    # Process a comment on a single line
    # in the form
    # // A comment

    # Get the double slash token.
    parser.tm.get_token(TokenType.COMMENT)

    # Get the end of line.
    parser.tm.get_token(TokenType.EOL)

    return True


def multi_line_comment_processor(parser: DocumentParser):
    # Process a multi-line comment
    # in the form
    # ////
    # A comment
    # on multiple lines
    # ////

    # Get the opening four slashes token.
    opening = parser.tm.get_token(TokenType.MULTILINE_COMMENT)

    # Collect everything before the next
    # four slashes.
    parser.tm.collect([Token(TokenType.MULTILINE_COMMENT, "////")])

    # Get the closing four slashes token.
    try:
        parser.tm.get_token(TokenType.MULTILINE_COMMENT, "////")
    except TokenError as exc:
        raise MauParserException(
            "Unclosed multi-line comment", opening.context
        ) from exc

    return True
