from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .parser import DocumentParser


from mau.nodes.document import HorizontalRuleNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.tokens.token import TokenType


def horizontal_rule_processor(parser: DocumentParser):
    # The horizontal rule ---

    # Get the horizontal rule token.
    rule = parser.tm.get_token(TokenType.HORIZONTAL_RULE)

    # Get the stored arguments.
    # Horizontal rules can receive arguments
    # only through the arguments manager.
    arguments = parser.arguments_buffer.pop_or_default()

    # Build the node info.
    info = NodeInfo(context=rule.context, **arguments.asdict())

    parser._save(
        Node(
            content=HorizontalRuleNodeContent(),
            info=info,
        )
    )

    return True
