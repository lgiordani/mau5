from __future__ import annotations

from mau.nodes.block import BlockNode
from mau.nodes.command import FootnotesItemNode, FootnotesNode
from mau.nodes.footnote import FootnoteNode


def default_footnote_unique_id(
    footnote: FootnoteNode,
) -> str:  # pragma: no cover
    """
    Return a unique ID for a footnote.
    """

    return footnote.name


class FootnotesManager:
    """This manager collects headers. and TOC nodes.
    When the manager process is run, all headers
    are given a unique ID (if not already initialised),
    Headers are then reshaped into a hierarchy,
    according to their level and position in the list,
    and both plain and hierarchical headers are added to
    each TOC node.
    """

    def __init__(self, footnote_unique_id_function=None):
        # This dictionary containes the footnotes created
        # through macros.
        self.footnotes: list[FootnoteNode] = []

        # This dictionary contains the body of each footnote
        # created through blocks.
        self.bodies: dict[str, BlockNode] = {}

        self.footnotes_lists: list[FootnotesNode] = []

        self.footnote_unique_id_function = (
            footnote_unique_id_function or default_footnote_unique_id
        )

    def add_footnote(self, footnote: FootnoteNode):
        """Add a single footnote to the list
        of managed footnotes."""
        self.footnotes.append(footnote)

    def add_footnotes(self, footnotes: list[FootnoteNode]):
        """Add a list of footnotes to the list
        of managed footnotes."""
        self.footnotes.extend(footnotes)

    def add_body(self, name: str, data: BlockNode):
        """Add the content of a footnote to
        the list of contents."""
        if name in self.bodies:
            raise ValueError(f"Footnote {name} has been already defined.")

        self.bodies[name] = data

    def add_footnotes_list(self, data: FootnotesNode):
        """Add a footnotes list node to
        the list of managed nodes."""
        self.footnotes_lists.append(data)

    def update(self, other: FootnotesManager):
        """Update footnotes, data, and footnotes nodes
        with those contained in another
        Footnotes Manager."""
        self.footnotes.extend(other.footnotes)
        self.bodies.update(other.bodies)
        self.footnotes_lists.extend(other.footnotes_lists)

    def process(self):
        # Process all footnotes. For each footnote
        # find the relative content, calculate
        # the public and explicit IDs, then
        # connect footnote and content.
        for number, footnote in enumerate(self.footnotes, start=1):
            # Find the content for this footnote.
            body = self.bodies[footnote.name]

            # Store the body inside the footnote.
            footnote.content = body.content

            # The public ID is the value
            # we will render in the document.
            footnote.public_id = str(number)

            # The private ID is the value
            # used to manage the connection
            # behind the scenes.
            footnote.private_id = self.footnote_unique_id_function(footnote)

        footnote_items = [
            FootnotesItemNode(footnote=footnote) for footnote in self.footnotes
        ]

        # Update all the nodes that list footnotes.
        for footnotes_list in self.footnotes_lists:
            footnotes_list.footnotes = footnote_items
