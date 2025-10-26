# Page nodes can be found at top level in a page

from mau.nodes.node import NodeContent

HORIZONTAL_RULE_HELP = """
Syntax:

([ARGS])?
---

The horizontal rule marks a separation between text sections
in the same document.
"""


class HorizontalRuleNodeContent(NodeContent):
    """A horizontal rule."""

    type = "horizontal_rule"


class WrapperNodeContent(NodeContent):
    type = "wrapper"
    allowed_keys = {"content": "The nodes inside the wrapper"}


class DocumentNodeContent(WrapperNodeContent):
    """A document.

    This node represents the full document.

    Arguments:
        content: the content of the document
    """

    type = "document"


class ContainerNodeContent(WrapperNodeContent):
    type = "container"

    def __init__(self, label: str):
        self.label = label

    def asdict(self):
        base = super().asdict()
        base.update({"label": self.label})

        return base
