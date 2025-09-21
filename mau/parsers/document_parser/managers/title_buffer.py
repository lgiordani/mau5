from __future__ import annotations

from mau.environment.environment import Environment
from mau.nodes.inline import SentenceNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.text_parser.parser import TextParser
from mau.text_buffer.context import Context


class TitleBuffer:
    def __init__(self):
        self.title: Node[SentenceNodeContent] | None = None

    def push(self, text: str, context: Context | None, environment: Environment | None):
        text_parser = TextParser.lex_and_parse(text, context, environment)

        if not text_parser.nodes:
            return

        self.title = Node(
            content=SentenceNodeContent(),
            children={"content": text_parser.nodes},
            info=NodeInfo(context=context),
        )

    def pop(self) -> Node[SentenceNodeContent]:
        node = self.title

        self.title = None

        return node
