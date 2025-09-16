from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .parser import DocumentParser

from mau.tokens.token import Token
from mau.nodes.block import BlockNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.base_parser.managers.tokens_manager import TokenError
from mau.parsers.base_parser.parser import MauParserException
from mau.text_buffer.context import Context
from mau.tokens.token import Token, TokenType


def _parse_block_content_update(
    parser: DocumentParser,
    node: Node[BlockNodeContent],
    content: Token | None,
):
    node.children["content"] = []

    if not content:
        return

    content_parser = parser.lex_and_parse(
        content.value,
        content.context,
        parser.environment,
    )

    # secondary_content_parser = DocumentParser.analyse(
    #     "\n".join(block.secondary_children),
    #     current_context,
    #     parser.environment,
    #     parent_node=block,
    #     parent_position="secondary",
    # )

    node.children["content"] = content_parser.nodes
    # block.secondary_children = secondary_content_parser.nodes

    # The footnote mentions and definitions
    # found in this block are part of the
    # main document. Import them.
    # parser.footnotes_manager.update(content_parser.footnotes_manager)

    # The internal links and headers
    # found in this block are part of the
    # main document. Import them.
    # parser.internal_links_manager.update(content_parser.internal_links_manager)

    # parser.toc_manager.update(content_parser.toc_manager)


def _parse_default_engine(
    parser: DocumentParser,
    node: Node[BlockNodeContent],
    content: Token | None,
):
    _parse_block_content_update(parser, node, content)
    parser._save(node)


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
    delimiter = parser.tm.get_token(TokenType.BLOCK)

    content: Token | None = None
    if parser.tm.peek_token().type == TokenType.TEXT:
        # Get the content of the block.
        content = parser.tm.get_token(TokenType.TEXT)

    # Get the closing delimiter.
    parser.tm.get_token(TokenType.BLOCK)

    # # Get the optional secondary content
    # secondary_content = parser.tm.collect_lines(
    #     [Token(TokenType.EOL), Token(TokenType.EOF)]
    # )

    # if delimiter in secondary_content:
    #     # This probably means that the input contains an error
    #     # and we are in a situation like

    #     # ----
    #     #
    #     # ----
    #     # Text
    #     # ----

    #     # Where ["Text", "----"] is considered the secondary content
    #     # of an empty block.
    #     parser._error(
    #         "Detected unclosed block (possibly before this line)"
    #     )  # pragma: no cover

    # Get the stored arguments.
    # Paragraphs can receive arguments
    # only through the arguments manager.
    arguments = parser.arguments_manager.pop_or_default()

    # arguments.set_names()

    # arguments = arguments.set_names()

    # block.title = parser._pop_title(block)

    # # Consume the arguments
    # args, kwargs, tags, subtype = parser.arguments_manager.pop()

    # # Check the control
    # if parser._pop_control() is False:
    #     return True

    # # If the subtype is an alias process it
    # alias = parser.block_aliases.get(subtype, {})
    # block.subtype = alias.get("subtype", subtype)
    # block_names = alias.get("mandatory_args", [])
    # block_defaults = alias.get("defaults", {})

    # args, kwargs = parser._set_names_and_defaults(
    #     args,
    #     kwargs,
    #     block_names,
    #     block_defaults,
    # )

    # Extract classes and convert them into a list
    if classes := arguments.named_args.pop("classes", []):
        classes = classes.split(",")

    # Extract the preprocessor
    preprocessor = arguments.named_args.pop("preprocessor", None)

    # Extract the engine
    engine = arguments.named_args.pop("engine", None)

    # block.args = args
    # block.kwargs = kwargs
    # block.tags = tags

    # Build the node info.
    info = NodeInfo(context=delimiter.context, **arguments.asdict())

    # Create the block
    node = Node(
        content=BlockNodeContent(
            classes=classes,
        ),
        info=info,
    )

    if title := parser.title_manager.pop():
        node.add_children({"title": [title]})

    match engine:
        case None:
            _parse_default_engine(parser, node, content)
        case _:
            raise parser._error(
                f"Engine {engine} is not available", context=delimiter.context
            )

    # elif block.engine == "mau":
    #     parser._parse_mau_engine(block)
    # elif block.engine == "source":
    #     parser._parse_source_engine(block)
    # elif block.engine == "footnote":
    #     parser._parse_footnote_engine(block)
    # elif block.engine == "raw":
    #     parser._parse_raw_engine(block)
    # elif block.engine == "group":
    #     parser._parse_group_engine(block)
    # else:

    return True
