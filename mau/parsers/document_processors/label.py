from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mau.parsers.document_parser import DocumentParser


from mau.parsers.text_parser import TextParser
from mau.token import TokenType


def label_processor(parser: DocumentParser):
    # Parse label text in the form
    #
    # . This is a title
    # or
    # .role This is a title
    #
    # The default role is "title".

    # Parse the mandatory dot
    prefix = parser.tm.get_token(
        TokenType.LABEL, value_check_function=lambda x: x.startswith(".")
    )

    role = prefix.value[1:] or "title"

    # Get the text of the title
    text_token = parser.tm.get_token(TokenType.TEXT)

    text_parser = TextParser.lex_and_parse(
        text_token.value,
        parser.environment,
        *text_token.context.start_position,
        text_token.context.source,
    )

    parser.label_buffer.push(role, text_parser.nodes)

    return True
