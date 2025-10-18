from __future__ import annotations

from collections import defaultdict
from typing import NewType

from mau.nodes.block import BlockGroupNodeContent, BlockNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.base_parser import MauParserException
from mau.text_buffer import Context

BlockGroup = NewType("BlockGroup", dict[str, Node[BlockNodeContent]])


class BlockGroupManager:
    def __init__(self):
        # This dictionary contains the block nodes
        # organised by group.
        self.groups: dict[str, BlockGroup] = defaultdict(dict)  # type: ignore[arg-type]

        # This list contains the group nodes that
        # will eventually render the group.
        self.group_nodes: list[Node[BlockGroupNodeContent]] = []

    def add_block(self, group: str, position: str, node: Node[BlockNodeContent]):
        """Add a block to the list of managed blocks."""
        block_group = self.groups[group]

        # Check if the position in the
        # block is already taken.
        if other_block := block_group.get(position):
            raise MauParserException(
                f"Position {position} is already taken in group {group} by the block at {other_block.info.context}",  # type: ignore[attr-defined]
                context=node.info.context,
            )

        block_group[position] = node

    def add_group_node(self, node: Node[BlockGroupNodeContent]):
        """Add a group node to the list of
        managed nodes."""
        self.group_nodes.append(node)

    def process(self):
        # Process all group nodes.
        # For each node, find if the relative
        # group exists and add all the nodes
        # in the group to the group node.

        for group_node in self.group_nodes:
            # Get the referenced group.
            group_name = group_node.content.name

            # Check if the requested group exists.
            if group_name not in self.groups:
                raise MauParserException(
                    message=f"The group named {group_name} does not exist.",
                    context=group_node.info.context,
                )

            # Add all blocks that mention this
            # group to the group node.
            for position, child_node in self.groups[group_name].items():
                group_node.add_children_at_position(
                    position, [child_node], allow_all=True
                )
