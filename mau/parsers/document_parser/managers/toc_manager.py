from __future__ import annotations

from mau.nodes.headers import HeaderNodeContent
from mau.nodes.node import Node
from mau.nodes.toc import TocItemNodeContent, TocNodeContent


def header_to_toc_item(header: Node[HeaderNodeContent]) -> Node[TocItemNodeContent]:
    return Node(
        content=TocItemNodeContent(
            level=header.content.level,  # type: ignore[attr-defined]
            anchor=header.content.anchor,  # type: ignore[attr-defined]
        ),
        info=header.info,
        children={"text": header.children["text"], "entries": []},
    )


def add_nodes_under_level(
    level: int,
    nodes: list[Node[HeaderNodeContent]],
    index: int,
    output: list[Node[TocItemNodeContent]],
) -> int:
    while index < len(nodes):
        # If the first node is at a higher or
        # equal level than the current one
        # stop the recursion.
        if nodes[index].content.level <= level:  # type: ignore[attr-defined]
            return index

        # Add the first node.
        node = header_to_toc_item(nodes[index])
        output.append(node)

        # Now perform the recursion on the
        # remaining nodes, adding the
        # children of the node that was
        # just added.
        index = add_nodes_under_level(
            level=nodes[index].content.level,  # type: ignore[attr-defined]
            nodes=nodes,
            index=index + 1,
            output=node.children["entries"],  # type: ignore[arg-type]
        )

    # There are no more nodes to process.
    # if not nodes:
    return index


class TocManager:
    def __init__(self):
        # This list contains the headers
        # found parsing a document
        self.headers: list[Node[HeaderNodeContent]] = []

        # This is the list of ::toc commands
        # that need to be updated once the ToC
        # has been processed
        self.toc_nodes: list[Node[TocNodeContent]] = []

    def add_header(self, node: Node[HeaderNodeContent]):
        self.headers.append(node)

    def add_toc_node(self, node: Node[TocNodeContent]):
        self.toc_nodes.append(node)

    def update(self, other: TocManager):
        self.headers.extend(other.headers)
        self.toc_nodes.extend(other.toc_nodes)

    def process(self):
        nested_headers: list[Node[TocItemNodeContent]] = []
        add_nodes_under_level(0, self.headers, 0, nested_headers)

        for toc_node in self.toc_nodes:
            toc_node.children["nested_entries"] = nested_headers  # type: ignore[assignment]
            toc_node.children["plain_entries"] = self.headers  # type: ignore[assignment]
