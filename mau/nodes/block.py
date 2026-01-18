from collections.abc import Sequence, Mapping
from mau.nodes.node import Node, NodeContentMixin, NodeInfo, NodeLabelsMixin, ValueNode


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
        classes=None,
        engine=None,
        content: Sequence[Node] | None = None,
        labels: Mapping[str, Sequence[Node]] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)
        NodeContentMixin.__init__(self, content)
        NodeLabelsMixin.__init__(self, labels)

        self.classes = classes or []
        self.engine = engine


class RawContentLineNode(ValueNode):
    """This contains a line of plain text
    that should be treated as raw data
    and left untouched.
    E.g. it shouldn't be escaped.
    """

    type = "raw-content-line"


class RawContentNode(Node, NodeContentMixin):
    """This contains a list of raw lines."""

    type = "raw-content"

    def __init__(
        self,
        lines: Sequence[RawContentLineNode] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)

        self.lines = lines or []
