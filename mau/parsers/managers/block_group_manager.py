from __future__ import annotations

from collections import defaultdict
from typing import NewType

from mau.nodes.block import BlockNodeData
from mau.nodes.commands import BlockGroupNodeData
from mau.nodes.node import Node

# This type is a dictionary of
# BlockNodeData objects, each
# listed under the position in
# in the group.
BlockGroup = NewType("BlockGroup", dict[str, Node[BlockNodeData]])


class BlockGroupManager:
    def __init__(self):
        # This dictionary contains the block nodes
        # organised by group.
        self.blocks: dict[str, BlockGroup] = defaultdict(dict)

        # type: ignore[arg-type]

        # This list contains the group nodes that
        # will eventually render the group.
        self.groups: list[BlockGroupNodeData] = []

    def add_block(self, group: str, position: str, node: Node[BlockNodeData]):
        """Add a block to the list of managed blocks."""
        block_group = self.blocks[group]

        # Check if the position in the
        # block is already taken.
        if block_group.get(position):
            raise ValueError(f"Position {position} is already taken in group {group}")

        block_group[position] = node

    def add_group(self, data: BlockGroupNodeData):
        """Add a group data to the list of
        managed datas."""
        self.groups.append(data)

    def process(self):
        # Process all group nodes.
        # For each node, find if the relative
        # group exists and add all the nodes
        # in the group to the group node.

        for group_node in self.groups:
            # Get the referenced group.
            group_name = group_node.name

            # Check if the requested group exists.
            if group_name not in self.blocks:
                # TODO replace this with a MauParserexception
                # when Node and NodeData are unified.
                raise ValueError(f"The group named {group_name} does not exist.")

            # Add all blocks that mention this
            # group to the group node.
            group_node.blocks.update(self.blocks[group_name])
