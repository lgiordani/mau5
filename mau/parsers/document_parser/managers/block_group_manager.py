from __future__ import annotations

from collections import defaultdict
from typing import NewType

from mau.nodes.block import BlockNodeContent
from mau.nodes.node import Node
from mau.parsers.base_parser.parser import MauParserException

BlockGroup = NewType("BlockGroup", dict[str, Node[BlockNodeContent]])


class BlockGroupManager:
    def __init__(self):
        # This list containes the internal links created
        # in the text through a macro.
        self.groups: dict[str, BlockGroup] = defaultdict(dict)  # type: ignore[arg-type]

    def add_block(self, group: str, position: str, node: Node[BlockNodeContent]):
        block_group = self.groups[group]

        if other_block := block_group.get(position):
            raise MauParserException(
                f"Position {position} is already taken in group {block_group} by the block at {other_block.info.context}",  # type: ignore[attr-defined]
                context=node.info.context,
            )

        block_group[position] = node
