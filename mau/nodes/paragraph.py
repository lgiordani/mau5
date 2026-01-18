from collections.abc import Sequence, Mapping
from mau.nodes.node import (
    Node,
    NodeContentMixin,
    NodeInfo,
    NodeLabelsMixin,
)


class ParagraphLineNode(Node, NodeContentMixin, NodeLabelsMixin):
    """
    This node represents the content of a line of a paragraph.
    """

    type = "paragraph-line"

    def __init__(
        self,
        content: Sequence[Node] | None = None,
        labels: Mapping[str, Sequence[Node]] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)
        NodeContentMixin.__init__(self, content)
        NodeLabelsMixin.__init__(self, labels)


class ParagraphNode(Node, NodeLabelsMixin):
    """A non-recursive container node.

    This node represents the content of a paragraph in a document.
    Its content is a list of lines (ParagraphLineNode)
    """

    type = "paragraph"

    def __init__(
        self,
        lines: Sequence[ParagraphLineNode] | None = None,
        labels: Mapping[str, Sequence[Node]] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)

        self.lines = lines or []

        NodeLabelsMixin.__init__(self, labels)
