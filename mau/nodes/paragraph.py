from mau.nodes.node import (
    Node,
    NodeData,
    NodeDataContentMixin,
    WrapperNodeData,
    NodeDataLabelsMixin,
)


class ParagraphNodeData(NodeData, NodeDataContentMixin, NodeDataLabelsMixin):
    """A non-recursive container node.

    This node represents the content of a paragraph in a document.
    Its content is a list of lines (ParagraphLineNodeData)
    """

    type = "paragraph"

    def __init__(
        self,
        content: list[Node] | None = None,
        labels: dict[str, Node[WrapperNodeData]] | None = None,
    ):
        super().__init__()

        NodeDataContentMixin.__init__(self, content)
        NodeDataLabelsMixin.__init__(self, labels)

    def asdict(self):
        base = super().asdict()

        NodeDataContentMixin.content_asdict(self, base)
        NodeDataLabelsMixin.content_asdict(self, base)

        return base


class ParagraphLineNodeData(NodeData, NodeDataContentMixin, NodeDataLabelsMixin):
    """
    This node represents the content of a line of a paragraph.
    """

    type = "paragraph-line"

    def __init__(
        self,
        content: list[Node] | None = None,
        labels: dict[str, Node[WrapperNodeData]] | None = None,
    ):
        super().__init__()

        NodeDataContentMixin.__init__(self, content)
        NodeDataLabelsMixin.__init__(self, labels)

    def asdict(self):
        base = super().asdict()

        NodeDataContentMixin.content_asdict(self, base)
        NodeDataLabelsMixin.content_asdict(self, base)

        return base
