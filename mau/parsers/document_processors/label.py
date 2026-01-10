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
    prefix = parser.tm.get_token(TokenType.LABEL)

    # Extract the name of the role
    role = prefix.value[1:] or "title"

    # Get the text of the label
    text_token = parser.tm.get_token(TokenType.TEXT)

    # Unpack the text initial position.
    start_line, start_column = text_token.context.start_position

    # Get the text source.
    source_filename = text_token.context.source

    # Parse the text of the label.
    text_parser = TextParser.lex_and_parse(
        text_token.value,
        parser.environment,
        start_line=start_line,
        start_column=start_column,
        source_filename=source_filename,
    )

    # Store the label node in the buffer.
    parser.label_buffer.push(role, text_parser.nodes)

    return True
