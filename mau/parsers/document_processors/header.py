from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mau.parsers.document_parser import DocumentParser


from mau.nodes.header import HeaderNode
from mau.nodes.node import NodeInfo
from mau.nodes.node_arguments import NodeArguments
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

    # Unpack the text initial position.
    start_line, start_column = text_token.context.start_position

    # Get the text source.
    source_filename = text_token.context.source

    # Replace variables
    preprocess_parser = PreprocessVariablesParser.lex_and_parse(
        text_token.value,
        parser.environment,
        start_line=start_line,
        start_column=start_column,
        source_filename=source_filename,
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
    # Names are set by the user and stored
    # in the headers manager. They are used to link
    # the header through the [header](name) macro.

    # Create the internal ID.
    # This uses the actual text contained in
    # the TextNode object.
    internal_id = arguments.named_args.pop("internal_id", None)

    # Extract the header id if specified.
    name = arguments.named_args.pop("name", None)

    # Find the context of the text.
    text_context = Context.merge_contexts(
        text_nodes[0].info.context, text_nodes[-1].info.context
    )

    # Find the context of the whole node.
    context = Context.merge_contexts(header.context, text_context)

    # The final node created by this parser.
    node = HeaderNode(
        level,
        internal_id=internal_id,
        name=name,
        content=text_nodes,
        source_text=text_token.value,
        info=NodeInfo(context=context),
        arguments=NodeArguments(**arguments.asdict()),
    )

    # Assign the given parent to each node.
    for i in text_nodes:
        i.parent = node

    # Extract labels from the buffer and
    # store them in the node data.
    parser.pop_labels(node)

    # Check the stored control
    if control := parser.control_buffer.pop():
        # If control is False, we need to stop
        # processing here and return without
        # saving any node.
        if not control.process(parser.environment):
            return True

    # If there is an id store the header node
    # to be matched with potential header links.
    if name:
        parser.header_links_manager.add_header(node)

    parser.toc_manager.add_header(node)

    parser._save(node)

    return True
