# from mau.nodes.node import (
#     Node,
#     NodeData,
#     NodeDataContentMixin,
#     NodeDataLabelsMixin,
#     WrapperNodeData,
# )
# 
# LIST_HELP = """
# Syntax:
# 
# ([URI+, ARGS])?
# (*+|#+) TEXT
# 
# The list prefix `*` or `#` creates a list item. The prefix can be
# specified multiple times to nest items, e.g.
# 
# * Item 1
# ** Item 1.1
# * Item2
# 
# The symbol `*` creates an unordered list, while the symbol `#`
# creates an ordered one. The two can be mixed, e.g.
# 
# # Numbered item 1
# ** Bullet point 1
# ** Bullet point 2
# ** Bullet point 3
# # Numbered item 2
# 
# Arguments:
# 
# * `start` - Can be a positive integer or "auto", defaults to "auto".
#             Controls the starting number for the first item of the list.
# """
# 
# 
# class ListItemNodeData(WrapperNodeData):
#     """An entry in a list."""
# 
#     type = "list_item"
# 
#     def __init__(self, level: int, content: list[Node] | None = None):
#         super().__init__(content)
# 
#         self.level = level
# 
#     def asdict(self):
#         base = super().asdict()
#         base["custom"]["level"] = self.level
# 
#         return base
# 
# 
# class ListNodeData(NodeData, NodeDataContentMixin, NodeDataLabelsMixin):
#     """A list."""
# 
#     type = "list"
# 
#     def __init__(
#         self,
#         ordered,
#         main_node=False,
#         start=1,
#         content: list[Node] | None = None,
#         labels: dict[str, list[Node]] | None = None,
#     ):
#         super().__init__()
#         self.ordered = ordered
#         self.main_node = main_node
#         self.start = start
# 
#         NodeDataContentMixin.__init__(self, content)
#         NodeDataLabelsMixin.__init__(self, labels)
# 
#     def asdict(self):
#         base = super().asdict()
#         base["custom"] = {
#             "ordered": self.ordered,
#             "main_node": self.main_node,
#             "start": self.start,
#         }
# 
#         NodeDataContentMixin.content_asdict(self, base)
#         NodeDataLabelsMixin.content_asdict(self, base)
# 
#         return base
