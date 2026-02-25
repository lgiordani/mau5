from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mau.parsers.document_parser import DocumentParser


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

    # Process the text of the header.
    text_nodes = parser._parse_text(
        text_token.value,
        text_token.context,
        parser.parent_node,
    )

    # Store the label node in the buffer.
    parser.label_buffer.push(role, text_nodes)

    return True
