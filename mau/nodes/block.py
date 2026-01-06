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
        content: list[Node] | None = None,
    ):
        super().__init__()

        self.classes = classes or []
        self.engine = engine
        self.preprocessor = preprocessor

        NodeDataContentMixin.__init__(self, content)

    def asdict(self):
        base = super().asdict()
        base["custom"] = {
            "classes": self.classes,
            "engine": self.engine,
            "preprocessor": self.preprocessor,
        }

        NodeDataContentMixin.content_asdict(self, base)

        return base


# class BlockSectionNodeData(NodeData):
#     """A section.

#     This node contains a section of a block.
#     """

#     type = "block-section"
#     allowed_keys = {
#         "content": "The text contained in this block.",
#     }

#     def __init__(
#         self,
#         name,
#     ):
#         self.name = name or []

#     def asdict(self):
#         base = super().asdict()
#         base.update(
#             {
#                 "name": self.name,
#             }
#         )

#         return base
