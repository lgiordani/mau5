from collections.abc import Mapping, Sequence

from mau.nodes.node import Node, NodeInfo, NodeLabelsMixin, ValueNode
from mau.nodes.node_arguments import NodeArguments


class RawLineNode(ValueNode):
    """This contains a line of plain text
    that should be treated as raw data
    and left untouched.
    E.g. it shouldn't be escaped.
    """

    type = "raw-line"


class RawNode(Node, NodeLabelsMixin):
    """This contains a list of raw lines."""

    type = "raw"

    def __init__(
        self,
        classes: Sequence[str] | None = None,
        content: Sequence[RawLineNode] | None = None,
        labels: Mapping[str, Sequence[Node]] | None = None,
        parent: Node | None = None,
        arguments: NodeArguments | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, arguments=arguments, info=info)
        NodeLabelsMixin.__init__(self, labels)

        self.content = content or []
        self.classes = classes or []
