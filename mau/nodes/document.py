# Page nodes can be found at top level in a page

from mau.nodes.node import NodeData, NodeDataLabelsMixin, Node, WrapperNodeData

HORIZONTAL_RULE_HELP = """
Syntax:

([ARGS])?
---

The horizontal rule marks a separation between text sections
in the same document.
"""


class HorizontalRuleNodeData(NodeData, NodeDataLabelsMixin):
    """A horizontal rule."""

    type = "horizontal_rule"

    def __init__(
        self,
        labels: dict[str, Node[WrapperNodeData]] | None = None,
    ):
        super().__init__()
        NodeDataLabelsMixin.__init__(self, labels)

    def asdict(self):
        base = super().asdict()
        NodeDataLabelsMixin.content_asdict(self, base)

        return base


# class WrapperNodeData(NodeData):
#     type = "wrapper"
#     allowed_keys = {"content": "The nodes inside the wrapper"}


# class DocumentNodeData(WrapperNodeData):
#     """A document.

#     This node represents the full document.

#     Arguments:
#         content: the content of the document
#     """

#     type = "document"


# class ContainerNodeData(WrapperNodeData):
#     type = "container"

#     def __init__(self, label: str):
#         self.label = label

#     def asdict(self):
#         base = super().asdict()
#         base.update({"label": self.label})

#         return base
