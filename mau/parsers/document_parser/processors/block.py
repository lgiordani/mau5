from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .parser import DocumentParser

from enum import Enum

from mau.parsers.base_parser.parser import BaseParser, MauParserException
from mau.environment.environment import Environment
from mau.nodes.block import BlockNodeContent
from mau.nodes.footnotes import FootnoteNodeContent
from mau.nodes.inline import RawNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.nodes.source import SourceLineNodeContent, SourceNodeContent
from mau.parsers.arguments_parser.parser import Arguments
from mau.text_buffer.context import Context
from mau.tokens.token import Token, TokenType


class EngineType(Enum):
    DEFAULT = "default"
    FOOTNOTE = "footnote"
    GROUP = "group"
    MAU = "mau"
    RAW = "raw"
    SOURCE = "source"


def parse_block_content(
    parser: DocumentParser,
    node: Node[BlockNodeContent],
    content: Token,
):
    content_parser = parser.lex_and_parse(
        content.value,
        content.context,
        Environment(),
    )
    content_parser.finalise()

    node.children["content"] = content_parser.nodes


def parse_block_content_update(
    parser: DocumentParser,
    node: Node[BlockNodeContent],
    content: Token,
):
    content_parser = parser.lex_and_parse(
        content.value,
        content.context,
        parser.environment,
    )

    node.children["content"] = content_parser.nodes

    # The footnote mentions and definitions
    # found in this block are part of the
    # main document. Import them.
    # parser.footnotes_manager.update(content_parser.footnotes_manager)

    # The internal links and headers
    # found in this block are part of the
    # main document. Import them.
    parser.toc_manager.update(content_parser.toc_manager)


def parse_default_engine(
    parser: DocumentParser,
    node: Node[BlockNodeContent],
    content: Token,
    block_context: Context,
    arguments: Arguments,
):
    parse_block_content_update(parser, node, content)


def parse_mau_engine(
    parser: DocumentParser,
    node: Node[BlockNodeContent],
    content: Token,
    block_context: Context,
    arguments: Arguments,
):
    parse_block_content(parser, node, content)


def parse_raw_engine(
    parser: DocumentParser,
    node: Node[BlockNodeContent],
    content: Token,
    block_context: Context,
    arguments: Arguments,
):
    # Engine "raw" doesn't process the content,
    # so we just pass it untouched in the form of
    # a RawNode per line.

    # A list of content lines (raw).
    content_lines = content.value.split("\n")

    # A list of raw content lines.
    raw_content: list[Node[RawNodeContent]] = []

    for number, line_content in enumerate(content_lines, start=1):
        line_context: Context | None = None

        if content.context:
            line_context = content.context.clone()
            line_context.start_line += number - 1
            line_context.end_line = line_context.start_line
            line_context.end_column = line_context.start_column + len(line_content)

        raw_content.append(
            Node(
                content=RawNodeContent(line_content),
                info=NodeInfo(context=line_context),
            )
        )

    node.children["content"] = raw_content


def parse_footnote_engine(
    parser: DocumentParser,
    node: Node[BlockNodeContent],
    content: Token,
    block_context: Context,
    arguments: Arguments,
):
    # The current block contains footnote data.
    # Extract the content and store it in
    # the footnotes manager.
    arguments.set_names(["name"])
    name = arguments.named_args.pop("name")

    content_parser = parser.lex_and_parse(
        content.value,
        content.context,
        parser.environment,
    )

    footnote_node = Node(
        content=FootnoteNodeContent(name),
        info=NodeInfo(context=block_context),
        children={"content": content_parser.nodes},
    )

    parser.footnotes_manager.add_data(footnote_node)


def parse_group_engine(
    parser: DocumentParser,
    node: Node[BlockNodeContent],
    content: Token,
    block_context: Context,
    arguments: Arguments,
):
    arguments.set_names(["group", "position"])

    group_name = arguments.named_args.pop("group")
    position = arguments.named_args.pop("position")

    content_parser = parser.lex_and_parse(
        content.value,
        content.context,
        parser.environment,
    )

    node = Node(
        content=BlockNodeContent(engine="group"),
        info=NodeInfo(context=block_context),
        children={"content": content_parser.nodes},
    )

    parser.block_group_manager.add_block(group_name, position, node)


def parse_source_engine(
    parser: DocumentParser,
    node: Node[BlockNodeContent],
    content: Token,
    block_context: Context,
    arguments: Arguments,
):
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

    # Source blocks must preserve the content literally.
    # However, there might be code that looks like a Mau directive,
    # and thus the user needs to escape it.
    # Which means that here we need to remove escaped characters
    # from directive-like code only.
    # Escape characters are preserved by source blocks as anything
    # else, but in this case the character should be removed.

    # A list of content lines (raw).
    content_lines = content.value.split("\n")

    # A list of code lines (after processing).
    code: list[Node[SourceLineNodeContent]] = []

    for number, line_content in enumerate(content_lines, start=1):
        line_number = str(number)

        line_context: Context | None = None

        if content.context:
            line_context = content.context.clone()
            line_context.start_line += number - 1
            line_context.end_line = line_context.start_line
            line_context.end_column = line_context.start_column + len(line_content)

        # A simple way to remove escapes from
        # directive-like code.
        if line_content.startswith(r"\::#"):
            line_content = line_content[1:]

        marker: str | None = None
        highlight_style: str | None = None

        if not line_content.endswith(marker_delimiter):
            create_source_line(code, line_number, line_content, line_context)
            continue

        # Split without the final delimiter
        splits = line_content[:-1].split(marker_delimiter)

        if len(splits) < 2:
            # It's a trap! There are no separators left.
            # Just add the line as it is.
            create_source_line(code, line_number, line_content, line_context)
            continue

        # Get the callout and the line
        marker = splits[-1]
        line_content = marker_delimiter.join(splits[:-1])

        if marker.startswith(highlight_prefix):
            highlight_style = marker[1:] or highlight_default_style
            marker = None

        create_source_line(
            code,
            line_number,
            line_content,
            line_context,
            marker=marker,
            highlight_style=highlight_style,
        )

    node.children["content"] = [
        Node(
            content=SourceNodeContent(language),
            children={"code": code},
            info=NodeInfo(context=content.context),
        )
    ]


def create_source_line(
    code: list[Node[SourceLineNodeContent]],
    line_number: str,
    line_content: str,
    line_context: Context | None,
    marker: str | None = None,
    highlight_style: str | None = None,
):
    # Prepare the source line
    source_line_node = Node(
        content=SourceLineNodeContent(
            line_number,
            line_content=line_content,
            marker=marker,
            highlight_style=highlight_style,
        ),
        info=NodeInfo(context=line_context),
    )

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

    # Check the stored control
    if control := parser.control_buffer.pop():
        # If control is False, we need to stop
        # processing here and return without
        # saving any node.
        if not control.process(parser.environment):
            return True

    # Find the final context.
    context = Context.merge_contexts(
        opening_delimiter.context, closing_delimiter.context
    )

    # Get the stored arguments.
    # Paragraphs can receive arguments
    # only through the arguments manager.
    arguments = parser.arguments_buffer.pop_or_default()

    # Extract classes and convert them into a list
    if classes := arguments.named_args.pop("classes", []):
        classes = classes.split(",")

    # Extract the preprocessor
    preprocessor = arguments.named_args.pop("preprocessor", None)

    # Extract the engine
    engine_name = arguments.named_args.pop("engine", "default")
    try:
        engine: EngineType = EngineType(engine_name)
    except ValueError as exc:
        raise MauParserException(
            f"Engine {engine_name} is not available", context=context
        ) from exc

    # Create the block
    node = Node(
        content=BlockNodeContent(
            classes=classes,
            engine=engine.value,
        ),
        children={"content": []},
    )

    if children := parser.children_buffer.pop():
        node.add_children(children, allow_all=True)

    if not content:
        node.info = NodeInfo(context=context, **arguments.asdict())

        parser._save(node)

        return True

    match engine:
        case EngineType.DEFAULT:
            parse_default_engine(parser, node, content, context, arguments)
            node.info = NodeInfo(context=context, **arguments.asdict())
            parser._save(node)
        case EngineType.FOOTNOTE:
            parse_footnote_engine(parser, node, content, context, arguments)
            node.info = NodeInfo(context=context, **arguments.asdict())
        case EngineType.GROUP:
            parse_group_engine(parser, node, content, context, arguments)
            node.info = NodeInfo(context=context, **arguments.asdict())
        case EngineType.MAU:
            parse_mau_engine(parser, node, content, context, arguments)
            node.info = NodeInfo(context=context, **arguments.asdict())
            parser._save(node)
        case EngineType.RAW:
            parse_raw_engine(parser, node, content, context, arguments)
            node.info = NodeInfo(context=context, **arguments.asdict())
            parser._save(node)
        case EngineType.SOURCE:
            parse_source_engine(parser, node, content, context, arguments)
            node.info = NodeInfo(context=context, **arguments.asdict())
            parser._save(node)
        case _:
            raise MauParserException(
                f"Engine {engine} is not available", context=context
            )

    return True
