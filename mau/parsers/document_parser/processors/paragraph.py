from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .parser import DocumentParser


from mau.text_buffer.context import Context
from mau.nodes.node import Node, NodeInfo
from mau.nodes.paragraph import ParagraphNodeContent
from mau.tokens.token import Token, TokenType
from mau.parsers.preprocess_variables_parser.parser import PreprocessVariablesParser


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

    # Check the stored control
    if control := parser.control_buffer.pop():
        # If control is False, we need to stop
        # processing here and return without
        # saving any node.
        if not control.process(parser.environment):
            return True

    text_token = Token.from_token_list(line_tokens, join_with=" ")

    # Get the stored arguments.
    # Paragraphs can receive arguments
    # only through the arguments manager.
    arguments = parser.arguments_buffer.pop_or_default()

    # Build the node info.
    info = NodeInfo(context=text_token.context, **arguments.asdict())

    # Process the text of the paragraph.
    text_nodes = parser._parse_text(text_token.value, context=text_token.context)

    node = Node(
        children={
            "content": text_nodes,
        },
        content=ParagraphNodeContent(),
        parent=parser.parent_node,
        info=info,
    )

    if children := parser.children_buffer.pop():
        node.add_children(children, allow_all=True)

    parser._save(node)

    return True
