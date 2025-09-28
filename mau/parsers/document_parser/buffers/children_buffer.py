from __future__ import annotations

from mau.environment.environment import Environment
from mau.nodes.node import Node, NodeContent
from mau.parsers.text_parser.parser import TextParser
from mau.text_buffer.context import Context


class ChildrenBuffer:
    def __init__(self):
        self.children: dict[str, list[Node[NodeContent]]] = {}

    def push(
        self,
        role: str,
        text: str,
        context: Context | None,
        environment: Environment | None,
    ):
        text_parser = TextParser.lex_and_parse(text, context, environment)

        self.children[role] = text_parser.nodes

    def pop(self) -> dict[str, list[Node[NodeContent]]]:
        nodes = self.children

        self.children = {}

        return nodes
