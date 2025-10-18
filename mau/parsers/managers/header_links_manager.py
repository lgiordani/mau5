from __future__ import annotations

from mau.nodes.headers import HeaderNodeContent
from mau.nodes.macros import MacroHeaderNodeContent
from mau.nodes.node import Node
from mau.parsers.base_parser import MauParserException


class HeaderLinksManager:
    """This manager collects headers and link macros.
    When the manager process is run, all macros
    are updated and given the correct header as child.
    """

    def __init__(self):
        # This list containes the internal links created
        # in the text through a macro.
        self._links: list[Node[MacroHeaderNodeContent]] = []

        # This dictionary contains the headers
        # flagged with an id
        self._headers: dict[str, Node[HeaderNodeContent]] = {}

    def add_header(self, header_id: str, node: Node[HeaderNodeContent]):
        """Add a single header to the list
        of managed headers. Check that the header
        ID is not already in use."""
        if header_id in self._headers:
            raise MauParserException(
                f"Duplicate header id detected: {header_id}", context=node.info.context
            )

        self._headers[header_id] = node

    def add_links(self, links: list[Node[MacroHeaderNodeContent]]):
        """Add the given list of links
        to the managed links."""
        self._links.extend(links)

    def update(self, other: HeaderLinksManager):
        """Update the headers and macro nodes
        with those contained in another
        Header Links Manager."""
        self.add_links(other._links)

        for header_id, node in other._headers.items():
            self.add_header(header_id, node)

    def process(self):
        # Process each macro node, find the
        # header it mentions in the list of
        # headers, and connect the two.
        for link in self._links:
            try:
                link.children["header"] = [self._headers[link.content.value]]  # type: ignore[attr-defined]
            except KeyError as exc:
                raise MauParserException(
                    f"Cannot find header with id {link.content.value}",  # type: ignore[attr-defined]
                    context=link.info.context,
                ) from exc
