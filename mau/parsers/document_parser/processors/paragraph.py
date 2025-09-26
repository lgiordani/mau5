from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .parser import DocumentParser


from mau.nodes.node import Node, NodeInfo
from mau.nodes.paragraph import ParagraphNodeContent
from mau.tokens.token import TokenType


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
    while parser.tm.peek_token().type == TokenType.TEXT:
        lines.append(parser.tm.get_token(TokenType.TEXT).value)

    # Check the stored control
    if control := parser.control_buffer.pop():
        # If control is False, we need to stop
        # processing here and return without
        # saving any node.
        if not control.process(parser.environment):
            return True

    # Multiple lines separated by a single
    # EOL form the same paragraph.
    # Join them with a space.
    text = " ".join(lines)

    # Get the stored arguments.
    # Paragraphs can receive arguments
    # only through the arguments manager.
    arguments = parser.arguments_buffer.pop_or_default()

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

    if nodes := parser.title_buffer.pop():
        node.add_children({"title": nodes})

    parser._save(node)

    return True
