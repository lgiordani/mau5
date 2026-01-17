from mau.nodes.node import Node, NodeInfo, NodeLabelsMixin, WrapperNode

HORIZONTAL_RULE_HELP = """
Syntax:

([ARGS])?
---

The horizontal rule marks a separation between text sections
in the same document.
"""


class HorizontalRuleNode(Node, NodeLabelsMixin):
    """A horizontal rule."""

    type = "horizontal-rule"

    def __init__(
        self,
        labels: dict[str, list[Node]] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)
        NodeLabelsMixin.__init__(self, labels)

    def asdict(self):
        base = super().asdict()
        NodeLabelsMixin.content_asdict(self, base)

        return base


class DocumentNode(WrapperNode):
    """A document.

    This node represents the full document.

    Arguments:
        content: the content of the document
    """

    type = "document"
