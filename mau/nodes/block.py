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
        classes=None,
        engine=None,
        content: list[Node] | None = None,
        labels: dict[str, list[Node]] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)
        NodeContentMixin.__init__(self, content)
        NodeLabelsMixin.__init__(self, labels)

        self.classes = classes or []
        self.engine = engine

    def asdict(self):
        base = super().asdict()
        base["custom"] = {
            "classes": self.classes,
            "engine": self.engine,
        }

        NodeContentMixin.content_asdict(self, base)
        NodeLabelsMixin.content_asdict(self, base)

        return base
