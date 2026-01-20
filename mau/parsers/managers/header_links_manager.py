from __future__ import annotations

from mau.nodes.header import HeaderNode
from mau.nodes.macro import MacroHeaderNode


class HeaderLinksManager:
    """This manager collects headers and link macros.
    When the manager process is run, all macros
    are updated and given the correct header as child.
    """

    def __init__(self):
        # This list containes the internal links created
        # in the text through a macro.
        self.links: list[MacroHeaderNode] = []

        # This dictionary contains the headers
        # flagged with an id
        self.headers: dict[str, HeaderNode] = {}

    def add_header(self, alias: str, data: HeaderNode):
        """Add a single header to the list
        of managed headers. Check that the header
        ID is not already in use."""
        if alias in self.headers:
            raise ValueError(
                f"Duplicate header id detected: {alias}",
            )

        self.headers[alias] = data

    def add_links(self, links: list[MacroHeaderNode]):
        """Add the given list of links
        to the managed links."""
        self.links.extend(links)

    def update(self, other: HeaderLinksManager):
        """Update the headers and macro nodes
        with those contained in another
        Header Links Manager."""
        self.add_links(other.links)

        for alias, node in other.headers.items():
            self.add_header(alias, node)

    def process(self):
        # Process each macro node, find the
        # header it mentions in the list of
        # headers, and connect the two.

        for link in self.links:
            try:
                target = self.headers[link.target_alias]

                link.header = target
                link.target_id = target.internal_id
            except KeyError as exc:
                raise ValueError(
                    f"Cannot find header with id {link.target_alias}",
                ) from exc
