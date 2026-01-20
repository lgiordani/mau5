from collections.abc import Mapping, Sequence

from mau.nodes.node import Node, NodeContentMixin, NodeInfo, NodeLabelsMixin


class BlockNode(Node, NodeLabelsMixin, NodeContentMixin):
    """A block.

    This node contains a generic block.

    Arguments:
        classes: a comma-separated list of classes
        engine: the engine used to render this block
        preprocessor: the preprocessor used for this block
    """

    type = "block"

    def __init__(
        self,
        classes: Sequence[str] | None = None,
        content: Sequence[Node] | None = None,
        labels: Mapping[str, Sequence[Node]] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)
        NodeContentMixin.__init__(self, content)
        NodeLabelsMixin.__init__(self, labels)

        self.classes = classes or []
