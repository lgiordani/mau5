import yaml

from mau.visitors.base_visitor import MauVisitorException
from mau.lexers.base_lexer import MauLexerException
from mau.parsers.base_parser import MauParserException
from mau.visitors.base_visitor import BaseVisitor
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
    def print_node_data(cls, node_data: dict):
        local_data = {}
        local_data.update(node_data)

        node_type = local_data.pop("_type")
        node_info = local_data.pop("_info")
        node_info.pop("context")

        print(f"Type: {node_type}")
        print(f"Info: {node_info}")
        print(f"Node values: {local_data}")

    @classmethod
    def print_nodes(cls, nodes: list[Node], indent: int = 0):
        bv = BaseVisitor()

        for node in nodes:
            result = bv.visit(node)

            print(yaml.dump(result, Dumper=yaml.Dumper))

    @classmethod
    def print_lexer_exception(cls, exc: MauLexerException):
        print(f"ERROR: {exc.message}")
        if exc.position:
            print(f"POSITION: {cls._adjust_position(exc.position)}")
        print()

    @classmethod
    def print_parser_exception(cls, exc: MauParserException):
        print(f"ERROR: {exc.message}")
        if exc.context:
            print(f"CONTEXT: {cls._adjust_context(exc.context)}")
            # TODO long help
        print()

    @classmethod
    def print_visitor_exception(cls, exc: MauVisitorException):
        print(f"Error while rendering node of type {exc.node.type}")
        print(f"Message: {exc.message}")

        if exc.node:
            print()
            print(f"Node context: {cls._adjust_context(exc.node.info.context)}")

        if exc.data:
            print()
            print("Node data:")
            cls.print_node_data(exc.data)

        if exc.additional_info:
            print()
            print(exc.additional_info)

        if exc.environment:
            print()
            print("Current environment:")
            print(exc.environment.asdict())
