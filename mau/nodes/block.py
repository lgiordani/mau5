from mau.nodes.node import Node, NodeData, NodeDataContentMixin


class BlockNodeData(NodeData, NodeDataContentMixin):
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
        sections: dict[str, list[Node]] | None = None,
    ):
        super().__init__()

        self.classes = classes or []
        self.engine = engine
        self.preprocessor = preprocessor
        self.sections = sections or {}

    def asdict(self):
        base = super().asdict()
        base["custom"] = {
            "classes": self.classes,
            "engine": self.engine,
            "preprocessor": self.preprocessor,
            "sections": {k: [i.asdict() for i in v] for k, v in self.sections.items()},
        }

        return base


# class BlockSectionNodeData(WrapperNodeData):
#     """A section.

#     This node contains a section of a block.
#     """

#     type = "block-section"
