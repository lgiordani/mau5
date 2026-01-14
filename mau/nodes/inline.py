# from mau.nodes.node import Node, NodeData, NodeDataContentMixin, ValueNodeData
# 
# 
# class WordNodeData(ValueNodeData):
#     """This is a single word, it's used internally
#     and eventually packed together with others into
#     a TextNode
#     """
# 
#     type = "word"
# 
# 
# class TextNodeData(ValueNodeData):
#     """This contains plain text and is created
#     as a collation of multiple WordNode objects
#     """
# 
#     type = "text"
# 
# 
# class RawNodeData(ValueNodeData):
#     """This contains plain text but the content
#     should be treated as raw data and left untouched.
#     E.g. it shouldn't be escaped.
#     """
# 
#     type = "raw"
# 
# 
# class VerbatimNodeData(ValueNodeData):
#     """This node contains verbatim text."""
# 
#     type = "verbatim"
# 
# 
# class StyleNodeData(NodeData, NodeDataContentMixin):
#     """Describes the style applied to a node."""
# 
#     type = "style"
# 
#     def __init__(self, style: str, content: list[Node] | None = None):
#         super().__init__()
#         self.style = style
#         NodeDataContentMixin.__init__(self, content)
# 
#     def asdict(self):
#         base = super().asdict()
#         base["custom"] = {
#             "style": self.style,
#         }
#         NodeDataContentMixin.content_asdict(self, base)
# 
#         return base
