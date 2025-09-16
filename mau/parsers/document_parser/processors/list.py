from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .parser import DocumentParser


from mau.nodes.lists import ListItemNodeContent, ListNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.tokens.token import Token, TokenType


def _process_list_nodes(parser: DocumentParser):
    # This parses all items of a list

    # Parse the header.
    header = parser.tm.get_token(TokenType.LIST)

    # Get the text of the item.
    text = parser.tm.get_token(TokenType.TEXT)

    # Parse the text of the item.
    content = parser._parse_text(
        text.value,
        context=text.context,
    )

    # Compute the level of the item
    level = len(header.value)

    nodes = []
    nodes.append(
        Node(
            content=ListItemNodeContent(str(level)),
            info=NodeInfo(context=header.context),
            children={"text": content},
        )
    )

    while parser.tm.peek_token() not in [
        Token(TokenType.EOF),
        Token(TokenType.EOL),
    ]:
        if len(parser.tm.peek_token().value) == level:
            # The new item is on the same level

            # Get the header
            header = parser.tm.get_token()

            # Get the text of the item.
            text = parser.tm.get_token(TokenType.TEXT)

            # Parse the text of the item.
            content = parser._parse_text(
                text.value,
                context=text.context,
            )

            # Compute the level of the item
            level = len(header.value)

            nodes.append(
                Node(
                    content=ListItemNodeContent(str(level)),
                    info=NodeInfo(context=header.context),
                    children={"text": content},
                )
            )

        elif len(parser.tm.peek_token().value) > level:
            # The new item is on a deeper level

            # Peek the header
            header = parser.tm.peek_token(TokenType.LIST)
            ordered = header.value[0] == "#"

            # Parse all the items at this level or higher.
            subnodes = _process_list_nodes(parser)

            nodes.append(
                Node(
                    content=ListNodeContent(ordered=ordered),
                    info=NodeInfo(context=header.context),
                    children={"nodes": subnodes},
                )
            )
        else:
            break

    return nodes


def list_processor(parser: DocumentParser):
    # Parse a list.
    # Lists can be ordered (using numbers)
    #
    # * One item
    # * Another item
    #
    # or unordered (using bullets)
    #
    # # Item 1
    # # Item 2
    #
    # The number of headers increases
    # the depth of each item
    #
    # # Item 1
    # ## Sub-Item 1.1
    #
    # Spaces before and after the header are ignored.
    # So the previous list can be also written
    #
    # # Item 1
    #   ## Sub-Item 1.1
    #
    # Ordered and unordered lists can be mixed.
    #
    # * One item
    # ## Sub Item 1
    # ## Sub Item 2
    #

    # Get the header and decide if it's a numbered or unnumbered list
    header = parser.tm.peek_token(TokenType.LIST)
    ordered = header.value[0] == "#"

    # Parse all the following items
    nodes = _process_list_nodes(parser)

    # Get the stored arguments.
    # Lists can receive arguments
    # only through the arguments manager.
    arguments = parser.arguments_manager.pop_or_default()

    # Check if the list has a forced start.
    if (start := arguments.named_args.pop("start", 1)) == "auto":  # TODO:get
        start = parser.latest_ordered_list_index
        parser.latest_ordered_list_index += len(nodes)
    else:
        start = int(start)
        parser.latest_ordered_list_index = len(nodes) + start

    node = Node(
        content=ListNodeContent(ordered=ordered, main_node=True, start=start),
        info=NodeInfo(context=header.context, **arguments.asdict()),
        children={"nodes": nodes},
    )

    parser._save(node)

    return True
