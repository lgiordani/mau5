from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .parser import DocumentParser


from mau.nodes.node import Node, NodeInfo
from mau.nodes.paragraph import ParagraphNodeContent
from mau.tokens.token import Token, TokenType


def paragraph_processor(parser: DocumentParser):
    # This parses a paragraph.
    # Paragraphs can be written on multiple lines and
    # end with an empty line.

    # Get the context of the first token we are going to process
    context = parser.tm.peek_token().context

    # Each line ends with EOL. This collects everything
    # before the EOL, then removes it. If the next token
    # is EOL we know that the paragraph is ended, otherwise
    # we continue to collect. If the token is EOF we
    # reached the end and we have to stop anyway.
    lines = []
    while parser.tm.peek_token() not in [
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]:
        # Get everything before the EOL.
        lines.append(
            parser.tm.collect_join(
                [
                    Token(TokenType.EOL),
                ]
            )
        )

        # Get the EOL.
        parser.tm.get_token(TokenType.EOL)

    # TODO
    # Check the control
    # if parser._pop_control() is False:
    #     return True

    # Multiple lines separated by a single
    # EOL form the same paragraph.
    # Join them with a space.
    text = " ".join(lines)

    # Get the stored arguments.
    # Paragraphs can receive arguments
    # only through the arguments manager.
    arguments = parser.arguments_manager.pop_or_default()

    # Build the node info.
    info = NodeInfo(
        context=context, position=parser.parent_position, **arguments.asdict()
    )

    # Process the text of the paragraph.
    text_nodes = parser._parse_text(text, context=context)

    node = Node(
        children={
            "content": text_nodes,
        },
        content=ParagraphNodeContent(),
        parent=parser.parent_node,
        info=info,
    )

    if title := parser.title_manager.pop():
        node.add_children({"title": [title]})

    parser._save(node)

    return True
