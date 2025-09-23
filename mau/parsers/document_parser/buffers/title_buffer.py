from __future__ import annotations

from mau.environment.environment import Environment
from mau.nodes.node import Node, NodeContent
from mau.parsers.text_parser.parser import TextParser
from mau.text_buffer.context import Context


class TitleBuffer:
    def __init__(self):
        self.title: list[Node[NodeContent]] = []

    def push(self, text: str, context: Context | None, environment: Environment | None):
        text_parser = TextParser.lex_and_parse(text, context, environment)

        self.title = text_parser.nodes

    def pop(self) -> list[Node[NodeContent]]:
        nodes = self.title

        self.title = []

        return nodes
