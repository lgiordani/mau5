from __future__ import annotations

import hashlib

from mau.nodes.commands import (
    TocItemNodeData,
    TocNodeData,
)
from mau.nodes.headers import HeaderNodeData


def default_header_internal_id(
    data: HeaderNodeData,
) -> str:  # pragma: no cover
    """
    Return a unique ID for a header.
    """

    # Get the source text of the header.
    text = data.source_text

    # Find the header level
    level = data.level

    hashed_value = hashlib.md5(f"{level} {text}".encode("utf-8")).hexdigest()[:8]

    return hashed_value


def add_nodes_under_level(
    level: int,
    nodes: list[HeaderNodeData],
    index: int,
    output: list[TocItemNodeData],
) -> int:
    # This recursive function transforms a list
    # of nodes into a hierarchy.

    # In this iteration, make sure we don't go
    # past the given number of nodes.
    while index < len(nodes):
        # If the first node is at a higher or
        # equal level than the current one
        # stop the recursion.
        if nodes[index].level <= level:
            return index

        # Add the first node.
        node = TocItemNodeData(nodes[index])
        output.append(node)

        # Now perform the recursion on the
        # remaining nodes, adding the
        # children of the node that was
        # just added.
        index = add_nodes_under_level(
            level=nodes[index].level,
            nodes=nodes,
            index=index + 1,
            output=node.entries,
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
        self.headers: list[HeaderNodeData] = []

        # This is the list of ::toc commands
        # that need to be updated once the ToC
        # has been processed
        self.toc_nodes: list[TocNodeData] = []

        self.header_internal_id_function = (
            header_internal_id_function or default_header_internal_id
        )

        self.nested_headers: list[TocItemNodeData] = []

    def add_header(self, data: HeaderNodeData):
        """Add a single header to the list
        of managed headers."""
        self.headers.append(data)

    def add_toc_node(self, data: TocNodeData):
        """Add a single TOC node to the list
        of managed TOC nodes."""
        self.toc_nodes.append(data)

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
            if header.internal_id is not None:
                continue

            # Create the unique internal ID.
            internal_id = self.header_internal_id_function(header)
            header.internal_id = internal_id

        # Create the nodes hierarchy.
        add_nodes_under_level(0, self.headers, 0, self.nested_headers)

        # Store the plain and hierarchical nodes
        # inside each TOC node.
        for toc_node in self.toc_nodes:
            toc_node.nested_entries = self.nested_headers
            toc_node.plain_entries = self.headers
