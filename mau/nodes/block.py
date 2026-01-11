from mau.nodes.node import Node, NodeData, NodeDataContentMixin, NodeDataLabelsMixin


class BlockNodeData(NodeData, NodeDataLabelsMixin):
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
        preprocessor=None,
        labels: dict[str, list[Node]] | None = None,
        sections: dict[str, list[Node]] | None = None,
    ):
        super().__init__()

        self.classes = classes or []
        self.engine = engine
        self.preprocessor = preprocessor
        self.sections = sections or {}

        NodeDataLabelsMixin.__init__(self, labels)

    def asdict(self):
        base = super().asdict()
        base["custom"] = {
            "classes": self.classes,
            "engine": self.engine,
            "preprocessor": self.preprocessor,
            "sections": {k: [i.asdict() for i in v] for k, v in self.sections.items()},
        }

        NodeDataLabelsMixin.content_asdict(self, base)

        return base
