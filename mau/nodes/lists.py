# from mau.nodes.node import NodeData, ValueNodeData

# LIST_HELP = """
# Syntax:

# ([URI+, ARGS])?
# (*+|#+) TEXT

# The list prefix `*` or `#` creates a list item. The prefix can be
# specified multiple times to nest items, e.g.

# * Item 1
# ** Item 1.1
# * Item2

# The symbol `*` creates an unordered list, while the symbol `#`
# creates an ordered one. The two can be mixed, e.g.

# # Numbered item 1
# ** Bullet point 1
# ** Bullet point 2
# ** Bullet point 3
# # Numbered item 2

# Arguments:

# * `start` - Can be a positive integer or "auto", defaults to "auto".
#             Controls the starting number for the first item of the list.
# """


# class ListItemNodeData(ValueNodeData):
#     """An entry in a list."""

#     type = "list_item"
#     value_key = "level"
#     allowed_keys = {"text": "The text of this list item"}


# class ListNodeData(NodeData):
#     """A list."""

#     type = "list"
#     allowed_keys = {"nodes": "The item nodes contained in this list. "}

#     def __init__(
#         self,
#         ordered,
#         main_node=False,
#         start=1,
#     ):
#         self.ordered = ordered
#         self.main_node = main_node
#         self.start = start

#     def asdict(self):
#         base = super().asdict()
#         base.update(
#             {
#                 "ordered": self.ordered,
#                 "main_node": self.main_node,
#                 "start": self.start,
#             }
#         )

#         return base
