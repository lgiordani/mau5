import yaml

from mau.nodes.node import Node
from mau.token import Token
from mau.visitors.base_visitor import BaseVisitor

from .base_formatter import BaseFormatter


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


class RawFormatter(BaseFormatter):
    type = "raw"

    @classmethod
    def print_tokens(cls, tokens: list[Token]):
        for token in tokens:
            print(
                f"{token.type} {repr(token.value)} {cls._adjust_context(token.context)}"
            )

    @classmethod
    def print_nodes(cls, nodes: list[Node], indent: int = 0):
        bv = BaseVisitor()

        for node in nodes:
            result = bv.visit(node)

            # print(result)
            print(yaml.dump(result, Dumper=NoAliasDumper))
