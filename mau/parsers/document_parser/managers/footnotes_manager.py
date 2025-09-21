from __future__ import annotations

import hashlib

from mau.nodes.macros import MacroFootnoteNodeContent
from mau.nodes.node import Node
from mau.nodes.footnotes import FootnoteNodeContent
from mau.parsers.base_parser.parser import MauParserException


class FootnotesManager:
    def __init__(self):
        # This dictionary containes the footnotes created
        # through macros.
        self.mentions: list[Node[MacroFootnoteNodeContent]] = []

        # This dictionary contains the content of footnote
        # created through blocks.
        self.data: dict[str, Node[FootnoteNodeContent]] = {}

        # This list contains all the footnote entries
        # that will be shown by a footnotes command.
        # self.footnotes = []

        # This is the list of ::footnotes commands
        # that need to be updated once footnotes
        # have been processed
        # self.command_nodes = []

        # This is the parser that contains the manager
        # self.parser = parser

    def add_mention(self, node: Node[MacroFootnoteNodeContent]):
        self.mentions.append(node)

    def add_data(self, node: Node[FootnoteNodeContent]):
        name = node.content.name

        if name in self.data:
            raise MauParserException(
                f"Footnote {name} has been already defined.", context=node.info.context
            )

        self.data[name] = node

    def process(self):
        for number, node in enumerate(self.mentions, start=1):
            name = node.content.name
            footnote_node = self.data[name]

            node.content.id = str(number)
            footnote_node.content.id = str(number)

            node.children["footnote"] = [footnote_node]


# def footnote_anchor(content):
#     return hashlib.md5(str(content).encode("utf-8")).hexdigest()[:8]
