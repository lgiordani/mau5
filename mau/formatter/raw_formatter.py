
import yaml

from mau.lexers.base_lexer import MauLexerException
from mau.nodes.node import Node
from mau.token import Token

from .base_formatter import BaseFormatter


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
        # space = "  " * indent

        for node in nodes:
            print(yaml.dump(node.asdict(recursive=True), Dumper=yaml.Dumper))

        # for node in nodes:
        #     print(f"{space}{node.content.asdict()} {node.info.asdict()}")
        #     for label, children in node.children.items():
        #         print(f"{space}  {label}:")
        #         cls.print_nodes(children, indent + 1)

    @classmethod
    def print_lexer_exception(cls, exc: MauLexerException):
        print(f"ERROR: {exc.message}")
        if exc.position:
            print(f"POSITION: {cls._adjust_position(exc.position)}")
        print()
