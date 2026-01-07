from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mau.parsers.document_parser import DocumentParser


from mau.nodes.document import HorizontalRuleNodeData
from mau.nodes.node import Node, NodeInfo
from mau.token import TokenType


def horizontal_rule_processor(parser: DocumentParser):
    # The horizontal rule ---

    # Get the horizontal rule token.
    rule = parser.tm.get_token(TokenType.HORIZONTAL_RULE)

    # Get the stored arguments.
    # Horizontal rules can receive arguments
    # only through the arguments manager.
    arguments = parser.arguments_buffer.pop_or_default()

    # Create the node.
    node = Node(
        data=HorizontalRuleNodeData(),
        info=NodeInfo(
            context=rule.context,
            **arguments.asdict(),
        ),
    )

    # Retrieve labels.
    if labels := parser.label_buffer.pop():
        node.data.labels = labels

    # Check the stored control
    if control := parser.control_buffer.pop():
        # If control is False, we need to stop
        # processing here and return without
        # saving any node.
        if not control.process(parser.environment):
            return True

    parser._save(node)

    return True
