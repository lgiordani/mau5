from __future__ import annotations

from mau.nodes.command import FootnotesItemNodeContent, FootnotesNodeContent
from mau.nodes.macros import MacroFootnoteNodeContent
from mau.nodes.node import Node
from mau.parsers.base_parser import MauParserException


def default_footnote_unique_id(
    node: Node[FootnotesItemNodeContent],
) -> str:  # pragma: no cover
    """
    Return a unique ID for a footnote.
    """

    return node.content.name


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
        self.mentions: list[Node[MacroFootnoteNodeContent]] = []

        # This dictionary contains the content of footnote
        # created through blocks.
        self.data: dict[str, Node[FootnotesItemNodeContent]] = {}

        self.footnotes_nodes: list[Node[FootnotesNodeContent]] = []

        self.footnote_unique_id_function = (
            footnote_unique_id_function or default_footnote_unique_id
        )

    def add_mention(self, node: Node[MacroFootnoteNodeContent]):
        """Add a single mention to the list
        of managed mentions."""
        self.mentions.append(node)

    def add_mentions(self, nodes: list[Node[MacroFootnoteNodeContent]]):
        """Add a list of mentions to the list
        of managed mentions."""
        self.mentions.extend(nodes)

    def add_data(self, node: Node[FootnotesItemNodeContent]):
        """Add the content of a footnote to
        the list of contents."""
        name = node.content.name

        if name in self.data:
            raise MauParserException(
                f"Footnote {name} has been already defined.", context=node.info.context
            )

        self.data[name] = node

    def add_footnotes_node(self, node: Node[FootnotesNodeContent]):
        """Add a footnotes list node to
        the list of managed nodes."""
        self.footnotes_nodes.append(node)

    def update(self, other: FootnotesManager):
        """Update mentions, data, and footnotes nodes
        with those contained in another
        Footnotes Manager."""
        self.mentions.extend(other.mentions)
        self.data.update(other.data)
        self.footnotes_nodes.extend(other.footnotes_nodes)

    def process(self):
        # Process all mentions. For each mention
        # find the relative content, calculate
        # the public and explicit IDs, then
        # connect mention and content.
        for number, node in enumerate(self.mentions, start=1):
            # Find the content for this mention.
            name = node.content.name
            footnote_node = self.data[name]

            # The public ID is the value
            # we will render in the document.
            node.content.public_id = str(number)
            footnote_node.content.public_id = str(number)

            # The private ID is the value
            # used to manage the connection
            # behind the scenes.
            node.content.private_id = self.footnote_unique_id_function(node)
            footnote_node.content.private_id = self.footnote_unique_id_function(node)

            # The mention is given the content
            # as a child, so that it's accessible
            # when rendering it.
            node.children["footnote"] = [footnote_node]

        # Update all the nodes that list footnotes.
        for footnotes_node in self.footnotes_nodes:
            footnotes_node.children["entries"] = self.data.values()
