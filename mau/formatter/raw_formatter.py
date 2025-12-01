import textwrap

from mau.lexers.base_lexer import MauLexerException
from mau.nodes.node import Node
from mau.parsers.base_parser import MauParserException
from mau.visitors.base_visitor import MauVisitorException
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
        space = "  " * indent

        for node in nodes:
            print(f"{space}{node.content.asdict()} {node.info.asdict()}")
            for label, children in node.children.items():
                print(f"{space}  {label}:")
                cls.print_nodes(children, indent + 1)

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
        print()
        print(exc.long_help)

    @classmethod
    def print_visitor_exception(cls, exc: MauVisitorException):
        print(
            textwrap.dedent(f"""
            Mau visitor error: {exc}
            ---
            NODE:
            """)
        )
        cls.print_nodes([exc.kwargs["node"]])
        print(
            textwrap.dedent(f"""
            TEMPLATES: {exc.kwargs["templates"]}
            """)
        )

        # TODO: This formatting should go into the exception itself
        # or into a method that is specific for that type of exception.
        # The problem is similar to the visitor parttern itself,
        # where we have the method accept in Node.
