from __future__ import annotations

import hashlib

from mau.nodes.headers import HeaderNodeContent
from mau.nodes.node import Node
from mau.nodes.toc import TocItemNodeContent, TocNodeContent


def default_header_unique_id(node: Node[HeaderNodeContent]) -> str:  # pragma: no cover
    """
    Return a unique ID for a header.
    """

    # Lowercase the text of the header.
    text_node = node.children["text"][0]
    text = text_node.content.value.lower()

    # Find the header level
    level = node.content.level

    hashed_value = hashlib.md5(f"{level} {text}".encode("utf-8")).hexdigest()[:8]

    return hashed_value


def header_to_toc_item(header: Node[HeaderNodeContent]) -> Node[TocItemNodeContent]:
    return Node(
        content=TocItemNodeContent(
            level=header.content.level,  # type: ignore[attr-defined]
            unique_id=header.content.unique_id,  # type: ignore[attr-defined]
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
    def __init__(self, header_unique_id_function=None):
        # This list contains the headers
        # found parsing a document
        self.headers: list[Node[HeaderNodeContent]] = []

        # This is the list of ::toc commands
        # that need to be updated once the ToC
        # has been processed
        self.toc_nodes: list[Node[TocNodeContent]] = []

        self.header_unique_id_function = (
            header_unique_id_function or default_header_unique_id
        )

        self.nested_headers: list[Node[TocItemNodeContent]] = []

    def add_header(self, node: Node[HeaderNodeContent]):
        self.headers.append(node)

    def add_toc_node(self, node: Node[TocNodeContent]):
        self.toc_nodes.append(node)

    def update(self, other: TocManager):
        self.headers.extend(other.headers)
        self.toc_nodes.extend(other.toc_nodes)

    def process(self):
        self.nested_headers = []

        for header in self.headers:
            if header.content.unique_id is not None:
                continue

            # Create the unique ID.
            unique_id = self.header_unique_id_function(header)
            header.content.unique_id = unique_id

        add_nodes_under_level(0, self.headers, 0, self.nested_headers)

        for toc_node in self.toc_nodes:
            toc_node.children["nested_entries"] = self.nested_headers  # type: ignore[assignment]
            toc_node.children["plain_entries"] = self.headers  # type: ignore[assignment]
