from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .parser import DocumentParser


from mau.nodes.headers import HeaderNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.preprocess_variables_parser import PreprocessVariablesParser
from mau.text_buffer import Context
from mau.token import TokenType


def header_processor(parser: DocumentParser):
    # Parse a header in the form
    #
    # = Header
    #
    # The number of equal signs is arbitrary
    # and represents the level of the header.
    # Headers are automatically assigned a unique ID
    # created using the provided function
    # parser.header_internal_id_function

    # Get all the equal signs.
    header = parser.tm.get_token(TokenType.HEADER)

    # Get the text of the header.
    text_token = parser.tm.get_token(TokenType.TEXT)

    # Calculate the level of the header.
    level = len(header.value)

    # Replace variables
    preprocess_parser = PreprocessVariablesParser.lex_and_parse(
        text_token.value,
        parser.environment,
        *text_token.context.start_position,
        text_token.context.source,
    )

    # The output of the preprocess parser.
    text_nodes = preprocess_parser.nodes

    # Get the stored arguments.
    # Headers can receive arguments
    # only through the arguments manager.
    arguments = parser.arguments_buffer.pop_or_default()

    # Internal IDs are used to create anchors
    # in the document. For example, they might be
    # the anchor name in HTML. They are stored
    # in the header itself.
    # External IDs are set by the user and stored
    # in the headers manager. They are used to link
    # the header through the [header](ID) macro.
    #
    # We could in theory use just the internal ID,
    # but since they are created automatically,
    # it would be difficult for the user to access
    # them. External IDs must be unique as well,
    # but they will be probably used less often.

    # Create the internal ID.
    # This uses the actual text contained in
    # the TextNodeContent object.
    internal_id = arguments.named_args.pop("internal_id", None)

    # Extract the header id if specified.
    external_id = arguments.named_args.pop("external_id", None)

    # Find the final context.
    context = Context.merge_contexts(header.context, text_nodes[-1].info.context)

    # Build the node info.
    info = NodeInfo(context=context, **arguments.asdict())

    node = Node(
        content=HeaderNodeContent(
            level,
            internal_id=internal_id,
            external_id=external_id,
        ),
        info=info,
        children={"text": text_nodes},
    )

    if label := parser.label_buffer.pop():
        node.add_children(label, allow_all=True)

    # Check the stored control
    if control := parser.control_buffer.pop():
        # If control is False, we need to stop
        # processing here and return without
        # saving any node.
        if not control.process(parser.environment):
            return True

    # If there is an id store the header node
    # to be matched with potential header links.
    if external_id:
        parser.header_links_manager.add_header(external_id, node)

    parser.toc_manager.add_header(node)

    parser._save(node)

    return True
