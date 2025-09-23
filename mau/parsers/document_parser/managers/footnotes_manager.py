from __future__ import annotations

from mau.nodes.footnotes import FootnoteNodeContent, FootnotesListNodeContent
from mau.nodes.macros import MacroFootnoteNodeContent
from mau.nodes.node import Node
from mau.parsers.base_parser.parser import MauParserException


def default_footnote_unique_id(
    node: Node[FootnoteNodeContent],
) -> str:  # pragma: no cover
    """
    Return a unique ID for a footnote.
    """

    return node.content.name


class FootnotesManager:
    def __init__(self, footnote_unique_id_function=None):
        # This dictionary containes the footnotes created
        # through macros.
        self.mentions: list[Node[MacroFootnoteNodeContent]] = []

        # This dictionary contains the content of footnote
        # created through blocks.
        self.data: dict[str, Node[FootnoteNodeContent]] = {}

        self.footnotes_list_nodes: list[Node[FootnotesListNodeContent]] = []

        self.footnote_unique_id_function = (
            footnote_unique_id_function or default_footnote_unique_id
        )

    def add_mention(self, node: Node[MacroFootnoteNodeContent]):
        self.mentions.append(node)

    def add_mentions(self, nodes: list[Node[MacroFootnoteNodeContent]]):
        self.mentions.extend(nodes)

    def add_data(self, node: Node[FootnoteNodeContent]):
        name = node.content.name

        if name in self.data:
            raise MauParserException(
                f"Footnote {name} has been already defined.", context=node.info.context
            )

        self.data[name] = node

    def add_footnotes_list_node(self, node: Node[FootnotesListNodeContent]):
        self.footnotes_list_nodes.append(node)

    def process(self):
        for number, node in enumerate(self.mentions, start=1):
            name = node.content.name
            footnote_node = self.data[name]

            node.content.public_id = str(number)
            footnote_node.content.public_id = str(number)

            node.content.private_id = self.footnote_unique_id_function(node)
            footnote_node.content.private_id = self.footnote_unique_id_function(node)

            node.children["footnote"] = [footnote_node]

        for footnotes_list_node in self.footnotes_list_nodes:
            footnotes_list_node.children["entries"] = self.data.values()
