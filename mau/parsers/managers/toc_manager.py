from __future__ import annotations

import hashlib

from mau.nodes.headers import HeaderNodeContent
from mau.nodes.node import Node
from mau.nodes.toc import TocItemNodeContent, TocNodeContent


def default_header_internal_id(
    node: Node[HeaderNodeContent],
) -> str:  # pragma: no cover
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
    # Convert a the content of the node
    # from HeadeNodeContent to TocItemNodeContent.

    return Node(
        content=TocItemNodeContent(
            level=header.content.level,  # type: ignore[attr-defined]
            internal_id=header.content.internal_id,  # type: ignore[attr-defined]
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
    # This recursive function transforms a list
    # of nodes into a hierarchy.

    # In this iteration, make sure we don't go
    # past the given number of nodes.
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
    """This manager collects headers and TOC nodes.
    When the manager process is run, all headers
    are given a unique ID (if not already initialised),
    Headers are then reshaped into a hierarchy,
    according to their level and position in the list,
    and both plain and hierarchical headers are added to
    each TOC node.
    """

    def __init__(self, header_internal_id_function=None):
        # This list contains the headers
        # found parsing a document
        self.headers: list[Node[HeaderNodeContent]] = []

        # This is the list of ::toc commands
        # that need to be updated once the ToC
        # has been processed
        self.toc_nodes: list[Node[TocNodeContent]] = []

        self.header_internal_id_function = (
            header_internal_id_function or default_header_internal_id
        )

        self.nested_headers: list[Node[TocItemNodeContent]] = []

    def add_header(self, node: Node[HeaderNodeContent]):
        """Add a single header to the list
        of managed headers."""
        self.headers.append(node)

    def add_toc_node(self, node: Node[TocNodeContent]):
        """Add a single TOC node to the list
        of managed TOC nodes."""
        self.toc_nodes.append(node)

    def update(self, other: TocManager):
        """Update the headers and toc nodes
        with those contained in another
        TOC Manager."""
        self.headers.extend(other.headers)
        self.toc_nodes.extend(other.toc_nodes)

    def process(self):
        self.nested_headers = []

        # Check that all headers have a
        # unique internal ID. If not, create it.
        for header in self.headers:
            if header.content.internal_id is not None:
                continue

            # Create the unique internal ID.
            internal_id = self.header_internal_id_function(header)
            header.content.internal_id = internal_id

        # Create the nodes hierarchy.
        add_nodes_under_level(0, self.headers, 0, self.nested_headers)

        # Store the plain and hierarchical nodes
        # inside each TOC node.
        for toc_node in self.toc_nodes:
            toc_node.children["nested_entries"] = self.nested_headers  # type: ignore[assignment]
            toc_node.children["plain_entries"] = self.headers  # type: ignore[assignment]
