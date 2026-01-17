from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mau.parsers.document_parser import DocumentParser

from mau.nodes.node import Node, NodeInfo
from mau.nodes.paragraph import ParagraphLineNode, ParagraphNode
from mau.text_buffer import Context
from mau.token import Token, TokenType


def paragraph_processor(parser: DocumentParser):
    # This parses a paragraph.
    # Paragraphs can be written on multiple lines and
    # end with an empty line.

    # Each line ends with EOL. This collects everything
    # before the EOL, then removes it. If the next token
    # is EOL we know that the paragraph is ended, otherwise
    # we continue to collect. If the token is EOF we
    # reached the end and we have to stop anyway.
    line_tokens: list[Token] = []
    while parser.tm.peek_token().type == TokenType.TEXT:
        line_tokens.append(parser.tm.get_token(TokenType.TEXT))

    # Fill a list of line nodes TODO
    line_nodes: list[Node] = []

    for line_token in line_tokens:
        # Build the node info.
        info = NodeInfo(context=line_token.context)

        # Process the text of the paragraph.
        text_nodes = parser._parse_text(line_token.value, context=line_token.context)

        line_node = ParagraphLineNode(
            content=text_nodes,
            parent=parser.parent_node,
            info=info,
        )

        line_nodes.append(line_node)

    # Get the stored arguments.
    # Paragraphs can receive arguments
    # only through the arguments manager.
    arguments = parser.arguments_buffer.pop_or_default()

    # Build the node info.
    info = NodeInfo(
        context=Context.merge_contexts(
            line_nodes[0].info.context,
            line_nodes[-1].info.context,
        ),
        **arguments.asdict(),
    )

    paragraph_node = ParagraphNode(
        content=line_nodes,
        parent=parser.parent_node,
        info=info,
    )

    # Extract labels from the buffer and
    # store them in the node data.
    if labels := parser.label_buffer.pop():
        paragraph_node.labels = labels

    # Check the stored control
    if control := parser.control_buffer.pop():
        # If control is False, we need to stop
        # processing here and return without
        # saving any node.
        if not control.process(parser.environment):
            return True

    parser._save(paragraph_node)

    return True
