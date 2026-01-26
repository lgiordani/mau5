from __future__ import annotations

from collections import defaultdict

from mau.nodes.block import BlockNode
from mau.nodes.command import BlockGroupNode
from mau.parsers.base_parser import MauParserException


class BlockGroupManager:
    def __init__(self):
        # This dictionary contains the block nodes
        # organised by group.
        self.blocks: dict[str, dict[str, BlockNode]] = defaultdict(dict)

        # type: ignore[arg-type]

        # This list contains the group nodes that
        # will eventually render the group.
        self.groups: list[BlockGroupNode] = []

    def add_block(self, group: str, position: str, node: BlockNode):
        """Add a block to the list of managed blocks."""
        block_group = self.blocks[group]

        # Check if the position in the
        # block is already taken.
        if block_group.get(position):
            raise ValueError(f"Position {position} is already taken in group {group}")

        block_group[position] = node

    def add_group(self, data: BlockGroupNode):
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
                raise MauParserException(
                    f"The group named {group_name} does not exist.",
                    group_node.info.context,
                )

            # Add all blocks that mention this
            # group to the group node.
            group_node.blocks.update(self.blocks[group_name])

            # Add each block that mention this
            # group to the group node and add
            # the group as the parent node.
            for position, block in self.blocks[group_name].items():
                block.parent = group_node
                group_node.blocks[position] = block
