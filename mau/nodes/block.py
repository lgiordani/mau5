# from mau.nodes.node import Node, NodeData, NodeDataContentMixin, NodeDataLabelsMixin
# 
# 
# class BlockNodeData(NodeData, NodeDataLabelsMixin, NodeDataContentMixin):
#     """A block.
# 
#     This node contains a generic block.
# 
#     Arguments:
#         classes: a comma-separated list of classes
#         engine: the engine used to render this block
#         preprocessor: the preprocessor used for this block
#     """
# 
#     type = "block"
# 
#     def __init__(
#         self,
#         classes=None,
#         engine=None,
#         labels: dict[str, list[Node]] | None = None,
#         content: list[Node] | None = None,
#     ):
#         super().__init__()
# 
#         self.classes = classes or []
#         self.engine = engine
# 
#         NodeDataContentMixin.__init__(self, content)
#         NodeDataLabelsMixin.__init__(self, labels)
# 
#     def asdict(self):
#         base = super().asdict()
#         base["custom"] = {
#             "classes": self.classes,
#             "engine": self.engine,
#         }
# 
#         NodeDataContentMixin.content_asdict(self, base)
#         NodeDataLabelsMixin.content_asdict(self, base)
# 
#         return base
