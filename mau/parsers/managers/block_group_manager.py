# from __future__ import annotations

# from collections import defaultdict
# from typing import NewType

# from mau.nodes.block import BlockNodeData
# from mau.nodes.commands import BlockGroupNodeData
# from mau.nodes.node import Node

# BlockGroup = NewType("BlockGroup", dict[str, BlockNodeData])


# class BlockGroupManager:
#     def __init__(self):
#         # This dictionary contains the block nodes
#         # organised by group.
#         self.groups: dict[str, BlockGroup] = defaultdict(dict)  # type: ignore[arg-type]

#         # This list contains the group nodes that
#         # will eventually render the group.
#         self.group_nodes: list[Node[BlockGroupNodeData]] = []

#     def add_block(self, group: str, position: str, data: BlockNodeData):
#         """Add a block to the list of managed blocks."""
#         block_group = self.groups[group]

#         # Check if the position in the
#         # block is already taken.
#         if block_group.get(position):
#             raise ValueError(f"Position {position} is already taken in group {group}")

#         block_group[position] = data

#     def add_group_node(self, data: BlockGroupNodeData):
#         """Add a group data to the list of
#         managed datas."""
#         self.group_nodes.append(data)

#     def process(self):
#         # Process all group nodes.
#         # For each node, find if the relative
#         # group exists and add all the nodes
#         # in the group to the group node.

#         for group_node in self.group_nodes:
#             # Get the referenced group.
#             group_name = group_node.name

#             # Check if the requested group exists.
#             if group_name not in self.groups:
#                 raise ValueError(
#                     message=f"The group named {group_name} does not exist.",
#                 )

#             # Add all blocks that mention this
#             # group to the group node.
#             for position, child_node in self.groups[group_name].items():
#                 group_node.add_children_at_position(
#                     position, [child_node], allow_all=True
#                 )
