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
        content: list[Node] | None = None,
        labels: dict[str, list[Node]] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)
        NodeContentMixin.__init__(self, content)
        NodeLabelsMixin.__init__(self, labels)

    def asdict(self):
        base = super().asdict()

        NodeContentMixin.content_asdict(self, base)
        NodeLabelsMixin.content_asdict(self, base)

        return base


class ParagraphNode(Node, NodeLabelsMixin):
    """A non-recursive container node.

    This node represents the content of a paragraph in a document.
    Its content is a list of lines (ParagraphLineNode)
    """

    type = "paragraph"

    def __init__(
        self,
        lines: list[ParagraphLineNode] | None = None,
        labels: dict[str, list[Node]] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)

        self.lines = lines or []

        NodeLabelsMixin.__init__(self, labels)

    def asdict(self):
        base = super().asdict()
        base["custom"]["lines"]: [i.asdict() for i in self.lines]

        NodeLabelsMixin.content_asdict(self, base)

        return base
