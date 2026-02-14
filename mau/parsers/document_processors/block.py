from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mau.parsers.document_parser import DocumentParser

from enum import Enum

from mau.nodes.block import BlockNode
from mau.nodes.node import Node, NodeInfo
from mau.nodes.node_arguments import NodeArguments
from mau.nodes.raw import RawLineNode, RawNode
from mau.nodes.source import (
    SourceLineNode,
    SourceMarkerNode,
    SourceNode,
)
from mau.parsers.base_parser import create_parser_exception
from mau.text_buffer import Context
from mau.token import Token, TokenType


class EngineType(Enum):
    DEFAULT = "default"
    RAW = "raw"
    SOURCE = "source"


def parse_block_content(
    parser: DocumentParser, content: Token, arguments: NodeArguments
) -> list[Node]:
    update = arguments.named_args.get("isolate", "true") == "false"

    # The parsing environment is
    # that of the external parser.
    environment = parser.environment

    # Unpack the token initial position.
    start_line, start_column = content.context.start_position

    # Get the token source.
    source_filename = content.context.source

    content_parser = parser.lex_and_parse(
        text=content.value,
        message_handler=parser.message_handler,
        environment=environment,
        start_line=start_line,
        start_column=start_column,
        source_filename=source_filename,
    )

    if update:
        # The footnote mentions and definitions
        # found in this block are part of the
        # main document. Import them.
        parser.footnotes_manager.update(content_parser.footnotes_manager)

        # The internal links and headers
        # found in this block are part of the
        # main document. Import them.
        parser.toc_manager.update(content_parser.toc_manager)

    return content_parser.nodes


def parse_default_engine(
    parser: DocumentParser, content: Token | None, arguments: NodeArguments
) -> list[Node]:
    node = BlockNode()

    if not content:
        return node

    # Parse the content of the block.
    nodes = parse_block_content(parser, content, arguments)

    # Assign the block as parent
    # of all nodes directly
    # contained in it.
    for i in nodes:
        i.parent = node

    # Assign the nodes to the block.
    node.content = nodes

    return node


def parse_raw_engine(
    parser: DocumentParser, content: Token | None, arguments: NodeArguments
) -> Node:
    # Engine "raw" doesn't process the content,
    # so we just pass it untouched in the form of
    # a RawNode per line.

    if not content:
        return RawNode()

    # A list of content lines (raw).
    content_lines = content.value.split("\n")

    # A list of raw content lines.
    raw_lines: list[RawLineNode] = []

    node = RawNode()

    for number, line_content in enumerate(content_lines, start=1):
        line_context = content.context.clone()
        line_context.start_line += number - 1
        line_context.end_line = line_context.start_line
        line_context.end_column = line_context.start_column + len(line_content)

        raw_lines.append(
            RawLineNode(
                line_content,
                info=NodeInfo(context=line_context),
                parent=node,
            )
        )

    # Assign the nodes to the block.
    node.content = raw_lines

    return node


def parse_source_engine(
    parser: DocumentParser, content: Token, arguments: NodeArguments
) -> Node:
    # Parse a source block in the form
    #
    # [engine=source]
    # ----
    # content
    # ----
    #
    # Source blocks support the following attributes
    #
    # language The language used to highlight the syntax.
    # marker_delimiter=":" The separator used by marker.
    # highlight_prefix="@" The special character to turn on highlight.
    #
    # Since Mau uses Pygments, the attribute language
    # is one of the languages supported by that tool.

    if not content:
        return SourceNode()

    # Get the delimiter for markers
    marker_delimiter = arguments.named_args.pop("marker_delimiter", ":")

    # Get the highlight prefix
    highlight_prefix = arguments.named_args.pop("highlight_marker", "@")

    # Get the default highlight style
    highlight_default_style = arguments.named_args.pop(
        "highlight_default_style", "default"
    )

    # Get the language
    arguments.set_names(["language"])
    language = arguments.named_args.pop("language", "text")

    # A list of content lines (raw).
    content_lines = content.value.split("\n")

    # A list of code lines (after processing).
    code: list[SourceLineNode] = []

    node = SourceNode(language)

    for number, line_content in enumerate(content_lines, start=1):
        line_number = str(number)

        line_context = content.context.clone()
        line_context.start_line += number - 1
        line_context.end_line = line_context.start_line
        line_context.end_column = line_context.start_column + len(line_content)

        marker: str | None = None
        highlight_style: str | None = None

        if not line_content.endswith(marker_delimiter):
            create_source_line(
                code,
                line_number,
                line_content,
                line_context,
                parent=node,
            )
            continue

        # Split without the final delimiter
        splits = line_content[:-1].split(marker_delimiter)

        if len(splits) < 2:
            # It's a trap! There are no separators left.
            # Just add the line as it is.
            create_source_line(
                code,
                line_number,
                line_content,
                line_context,
                parent=node,
            )
            continue

        # Get the callout and the line
        marker = splits[-1]
        line_content = marker_delimiter.join(splits[:-1])

        if marker.startswith(highlight_prefix):
            highlight_style = marker[1:] or highlight_default_style
            marker = None

        marker_node: SourceMarkerNode | None = None

        # If there is a marker, change the line
        # context to remove the marker.
        if marker:
            # Take into account the two colons.
            marker_length = len(marker) + 2

            # Calculate the line length.
            line_length = len(line_content)

            # Clone the line context.
            marker_context = line_context.clone()

            # Remove the marker from the end
            # of the line context.
            line_context.end_column -= marker_length

            # Remove the line from the
            # marker context.
            marker_context.start_column += line_length

            marker_node = SourceMarkerNode(
                marker,
                info=NodeInfo(context=marker_context),
            )

        create_source_line(
            code,
            line_number,
            line_content,
            line_context,
            parent=node,
            marker_node=marker_node,
            highlight_style=highlight_style,
        )

    node.content = code
    node.info = NodeInfo(context=content.context)

    return node


def create_source_line(
    code: list[SourceLineNode],
    line_number: str,
    line_content: str,
    line_context: Context,
    parent: Node,
    marker_node: SourceMarkerNode | None = None,
    highlight_style: str | None = None,
):
    # Prepare the source line
    source_line_node = SourceLineNode(
        line_number,
        line_content=line_content,
        highlight_style=highlight_style,
        info=NodeInfo(context=line_context),
        parent=parent,
    )

    if marker_node:
        source_line_node.marker = marker_node

    code.append(source_line_node)


def block_processor(parser: DocumentParser):
    # Parse a block in the form
    #
    # [block_type]
    # ----
    # Content
    # ----
    # Optional secondary content
    #
    # Blocks are delimited by 4 consecutive identical characters.

    # Get the opening delimiter.
    opening_delimiter = parser.tm.get_token(TokenType.BLOCK)

    content: Token | None = None
    if parser.tm.peek_token().type == TokenType.TEXT:
        # Get the content of the block.
        content = parser.tm.get_token(TokenType.TEXT)

    # Get the closing delimiter.
    closing_delimiter = parser.tm.get_token(TokenType.BLOCK)

    # Find the final context.
    context = Context.merge_contexts(
        opening_delimiter.context, closing_delimiter.context
    )

    # Get the stored arguments.
    # Paragraphs can receive arguments
    # only through the arguments manager.
    arguments = parser.arguments_buffer.pop_or_default()

    # Extract classes and convert them into a list
    classes_str = arguments.named_args.pop("classes", "")
    classes = classes_str.split(",") if classes_str else []

    # Extract the engine
    engine_name = arguments.named_args.pop("engine", "default")
    try:
        engine: EngineType = EngineType(engine_name)
    except ValueError as exc:
        raise create_parser_exception(
            f"Engine '{engine_name}' is not available.",
            context=context,
        ) from exc

    match engine:
        # Real engine: decides how the content is processed
        case EngineType.DEFAULT:
            node = parse_default_engine(parser, content, arguments)

        case EngineType.RAW:  # Real engine: decides how the content is processed
            node = parse_raw_engine(parser, content, arguments)

        case EngineType.SOURCE:  # Real engine: decides how the content is processed
            node = parse_source_engine(parser, content, arguments)

    node.classes = classes

    # Extract labels from the buffer and
    # store them in the node data.
    parser.pop_labels(node)

    footnote_name = arguments.named_args.get("footnote")

    if footnote_name:
        parser.footnotes_manager.add_body(footnote_name, node)

        return True

    group_name = arguments.named_args.get("group")
    position = arguments.named_args.get("position")

    node.info = NodeInfo(context=context)
    node.arguments = NodeArguments(**arguments.asdict())

    if group_name and position:
        parser.block_group_manager.add_block(group_name, position, node)

        return True

    # Check the stored control
    if control := parser.control_buffer.pop():
        # If control is False, we need to stop
        # processing here and return without
        # saving any node.
        if not control.process(parser.environment):
            return True

    parser._save(node)

    return True
