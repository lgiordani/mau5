from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .parser import DocumentParser


from mau.nodes.headers import HeaderNodeContent
from mau.nodes.inline import SentenceNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.preprocess_variables_parser.parser import PreprocessVariablesParser
from mau.tokens.token import TokenType


def header_processor(parser: DocumentParser):
    # Parse a header in the form
    #
    # = Header
    #
    # The number of equal signs is arbitrary
    # and represents the level of the header.
    # Headers are automatically assigned an anchor
    # created using the provided function parser.header_anchor

    # Get all the equal signs.
    header = parser.tm.get_token(TokenType.HEADER)

    # Get the text of the header.
    text_token = parser.tm.get_token(TokenType.TEXT)

    # Calculate the level of the header.
    level = len(header.value)

    # Replace variables
    preprocess_parser = PreprocessVariablesParser.lex_and_parse(
        text_token.value,
        text_token.context,
        parser.environment,
    )

    # If the preprocessor doesn't return any
    # node we can stop here.
    if not preprocess_parser.nodes:
        return []

    # The preprocess parser outputs a single node.
    text_node = preprocess_parser.nodes[0]

    # Get the content of the text_node
    text = text_node.content

    # # Check the control
    # if parser._pop_control() is False:
    #     return True

    # Get the stored arguments.
    # Headers can receive arguments
    # only through the arguments manager.
    arguments = parser.arguments_manager.pop_or_default()

    # Create the anchor.
    # This uses the actual text contained in
    # the TextNodeContent object.
    anchor = arguments.named_args.pop(  # TODO get
        "anchor", parser.header_anchor(text.value, level)
    )

    # Extract the header id if specified.
    header_id = arguments.named_args.get("id", None)

    # Build the node info.
    info = NodeInfo(context=header.context, **arguments.asdict())

    node = Node(
        content=HeaderNodeContent(level, anchor),
        info=info,
        children={
            "text": [
                Node(
                    content=SentenceNodeContent(),
                    children={"content": [text_node]},
                    info=NodeInfo(context=text_token.context),
                )
            ]
        },
    )

    # If there is an id store the header node
    # to be matched with potential header links.
    if header_id:
        parser.internal_links_manager.add_header(header_id, node)

    parser.toc_manager.add_header(node)

    parser._save(node)

    return True
