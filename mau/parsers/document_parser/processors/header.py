from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .parser import DocumentParser


from mau.text_buffer.context import Context
from mau.nodes.headers import HeaderNodeContent
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
    # Headers are automatically assigned a unique ID
    # created using the provided function
    # parser.header_unique_id_function

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

    # The output of the preprocess parser.
    text_nodes = preprocess_parser.nodes

    # Check the stored control
    if control := parser.control_buffer.pop():
        # If control is False, we need to stop
        # processing here and return without
        # saving any node.
        if not control.process(parser.environment):
            return True

    # Get the stored arguments.
    # Headers can receive arguments
    # only through the arguments manager.
    arguments = parser.arguments_buffer.pop_or_default()

    # Create the unique ID.
    # This uses the actual text contained in
    # the TextNodeContent object.
    unique_id = arguments.named_args.pop("unique_id", None)

    # Extract the header id if specified.
    header_id = arguments.named_args.get("id", None)

    # Find the final context.
    context = Context.merge_contexts(header.context, text_nodes[-1].info.context)

    # Build the node info.
    info = NodeInfo(context=context, **arguments.asdict())

    node = Node(
        content=HeaderNodeContent(level, unique_id),
        info=info,
        children={"text": text_nodes},
    )

    # If there is an id store the header node
    # to be matched with potential header links.
    if header_id:
        parser.header_links_manager.add_header(header_id, node)

    parser.toc_manager.add_header(node)

    parser._save(node)

    return True
