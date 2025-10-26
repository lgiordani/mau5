from __future__ import annotations

import itertools
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .parser import DocumentParser

from enum import Enum

from collections import defaultdict
from mau.parsers.base_parser import BaseParser, MauParserException
from mau.environment.environment import Environment
from mau.nodes.block import BlockNodeContent
from mau.nodes.command import FootnotesItemNodeContent
from mau.nodes.inline import RawNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.nodes.source import (
    SourceLineNodeContent,
    SourceNodeContent,
    SourceMarkerNodeContext,
)
from mau.parsers.arguments_parser import Arguments
from mau.text_buffer import Context
from mau.token import Token, TokenType


DEFAULT_SECTION_PREFIX = "++ "


class EngineType(Enum):
    DEFAULT = "default"
    FOOTNOTE = "footnote"
    GROUP = "group"
    MAU = "mau"
    RAW = "raw"
    SOURCE = "source"


def _get_section_name(line: str, prefix: str) -> str | None:
    if not line.startswith(prefix):
        return None

    return line.replace(prefix, "")


def parse_block_content_sections(content: Token) -> dict[str, Token]:
    # Convert the text token to a list of text tokens.

    # Create a list of TEXT tokens from
    # the single token.
    tokens = content.to_token_list()

    # This function is run only when
    # the user turns on sections.
    # This means that the first line
    # must contain a section, otherwise
    # there is an error.
    first_section_name = _get_section_name(tokens[0].value, DEFAULT_SECTION_PREFIX)
    if not first_section_name:
        raise MauParserException(
            "The first line of the block must contain a section declaration.",
            context=tokens[0].context,
        )

    # This splits the list of tokens into
    # groups of normal lines or section lines.
    # E.g.
    #
    # ++ Section 1
    # Some text.
    # ++ Section 2
    # Some text 2a.
    # Some text 2b.
    # ++ Section 3
    # ++ Section 4
    # Some text 4.
    #
    # becomes
    #
    # True [Token("++ Section 1")]
    # False [Token("Some text.")]
    # True [Token("++ Section 2")]
    # False [Token("Some text 2a."), Token("Some text 2b.")]
    # True [Token("++ Section 3"), Token("++ Section 4")]
    # False [Token("Some text 4."2)]
    section_groups = itertools.groupby(tokens, lambda x: x.value.startswith("++ "))

    # This is the final dictionary
    # of sections.
    sections: dict[str, Token] = {}

    # This is the current section name.
    current_section_name: str = ""

    # Loop through all groups.
    # If they are a group of sections
    # create all of them. If they
    # are a group of lines merge
    # them into a single token
    # and add that to the section.
    for section_flag, tokens in section_groups:
        # The list of tokens contains
        # a list of section lines.
        if section_flag:
            # Loop through all sections
            # and create each one of them
            # in the sections dictionary.
            # Store the name so that
            # the next batch of normal
            # line tokens can be added to it.
            for section_token in tokens:
                current_section_name: str = section_token.value.replace(
                    DEFAULT_SECTION_PREFIX, ""
                )

                sections[current_section_name] = Token(
                    TokenType.TEXT, "", section_token.context
                )

            continue

        # We reach this line if the group
        # contains normal lines. We need
        # to store them all under the
        # last section.
        sections[current_section_name] = Token.from_token_list(
            list(tokens), join_with="\n"
        )

    return sections


def parse_block_content(
    parser: DocumentParser,
    node: Node[BlockNodeContent],
    content: Token,
    arguments: Arguments,
    update: bool,
):
    # Sections are disabled by default.
    # The option `enable_sections` set to
    # "true" turns them on.
    if arguments.named_args.get("enable_sections", "false") == "true":
        sections = parse_block_content_sections(content)
    else:
        # If there are no sections, we
        # fake a single section called
        # "content" so that the next code
        # results in the standard block
        # setup with children under
        # that kay.
        sections = {"content": content}

    # The parsing environment
    # can be either the one contained
    # in the external parser or an empty
    # one. This depends if the
    # current parsing is updating
    # the external parser or not.
    environment = parser.environment if update else Environment()

    # Loop through all sections,
    # parse the content, and add
    # the children to the block node.
    for name, token in sections.items():
        content_parser = parser.lex_and_parse(
            token.value,
            environment,
            *token.context.start_position,
            token.context.source,
        )
        content_parser.finalise()

        # Sections names are not conventional,
        # so we need to allow them when we
        # add the nodes as children.
        node.add_children_at_position(name, content_parser.nodes, allow_all=True)

    if update:
        # The footnote mentions and definitions
        # found in this block are part of the
        # main document. Import them.
        parser.footnotes_manager.update(content_parser.footnotes_manager)

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
    parse_block_content(parser, node, content, arguments, update=True)


def parse_mau_engine(
    parser: DocumentParser,
    node: Node[BlockNodeContent],
    content: Token,
    block_context: Context,
    arguments: Arguments,
):
    parse_block_content(parser, node, content, arguments, update=False)


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
        parser.environment,
        *content.context.start_position,
        content.context.source,
    )

    footnote_node = Node(
        content=FootnotesItemNodeContent(name),
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
        parser.environment,
        *content.context.start_position,
        content.context.source,
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

        marker_node: Node[SourceMarkerNodeContext] | None = None

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

            marker_node = Node(
                content=SourceMarkerNodeContext(marker),
                info=NodeInfo(context=marker_context),
            )

        create_source_line(
            code,
            line_number,
            line_content,
            line_context,
            marker_node=marker_node,
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
    line_context: Context,
    marker_node: Node[SourceMarkerNodeContext] | None = None,
    highlight_style: str | None = None,
):
    # Prepare the source line
    source_line_node = Node(
        content=SourceLineNodeContent(
            line_number,
            line_content=line_content,
            highlight_style=highlight_style,
        ),
        info=NodeInfo(context=line_context),
    )

    if marker_node:
        source_line_node.add_children({"marker": [marker_node]})

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

    if label := parser.label_buffer.pop():
        node.add_children(label, allow_all=True)

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
        # This has been checked before but is required to
        # check the full type value space.
        case _:  # pragma: no cover
            raise MauParserException(
                f"Engine {engine} is not available", context=context
            )

    return True
