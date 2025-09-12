from __future__ import annotations

from mau.nodes.headers import HeaderNodeContent
from mau.nodes.node import Node
from mau.nodes.toc import TocNodeContent


def add_nodes_under_level(
    level: int,
    nodes: list[Node[HeaderNodeContent]],
    index: int,
    output: list[Node[HeaderNodeContent]],
) -> int:
    while index < len(nodes):
        # If the first node is at a higher or
        # equal level than the current one
        # stop the recursion.
        if nodes[index].content.level <= level:  # type: ignore[attr-defined]
            return index

        # Add the first node.
        output.append(nodes[index])

        # Now perform the recursion on the
        # remaining nodes, adding the
        # children of the node that was
        # just added.
        index = add_nodes_under_level(
            level=nodes[index].content.level,  # type: ignore[attr-defined]
            nodes=nodes,
            index=index + 1,
            output=nodes[index].children["entries"],  # type: ignore[arg-type]
        )

    # There are no more nodes to process.
    # if not nodes:
    return index


class TocManager:
    def __init__(self):
        # This list contains the headers
        # found parsing a document
        self._headers: list[Node[HeaderNodeContent]] = []

        # This is the list of ::toc commands
        # that need to be updated once the ToC
        # has been processed
        self._toc_nodes: list[Node[TocNodeContent]] = []

    def add_header(self, node: Node[HeaderNodeContent]):
        self._headers.append(node)

    def add_toc_node(self, node: Node[TocNodeContent]):
        self._toc_nodes.append(node)

    def update(self, other: TocManager):
        self._headers.extend(other._headers)
        self._toc_nodes.extend(other._toc_nodes)

    def process(self):
        nested_headers: list[Node[HeaderNodeContent]] = []
        add_nodes_under_level(0, self._headers, 0, nested_headers)

        for toc_node in self._toc_nodes:
            toc_node.children["nested_entries"] = nested_headers  # type: ignore[assignment]
            toc_node.children["plain_entries"] = self._headers  # type: ignore[assignment]
