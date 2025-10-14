from mau.lexers.text_lexer import TextLexer
from mau.nodes.inline import TextNodeContent
from mau.nodes.macros import MacroNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.text_parser import TextParser
from mau.test_helpers import (
    compare_nodes,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(TextLexer, TextParser)

runner = parser_runner_factory(TextLexer, TextParser)


def test_generic_macro():
    source = "[macroname](value1,value2)"

    expected = [
        Node(
            content=MacroNodeContent("macroname", unnamed_args=["value1", "value2"]),
            info=NodeInfo(context=generate_context(0, 0, 0, 26)),
        )
    ]

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        expected,
    )


def test_generic_macro_incomplete():
    source = "[macroname](value1"

    expected = [
        Node(
            content=TextNodeContent("[macroname](value1"),
            info=NodeInfo(context=generate_context(0, 0, 0, 18)),
        ),
    ]

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        expected,
    )


def test_generic_macro_named_arguments():
    source = "[macroname](name,arg1=value1)"

    expected = [
        Node(
            content=MacroNodeContent(
                "macroname",
                unnamed_args=["name"],
                named_args={"arg1": "value1"},
            ),
            info=NodeInfo(context=generate_context(0, 0, 0, 29)),
        )
    ]

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        expected,
    )


def test_generic_macro_without_arguments():
    source = "[macroname]()"

    expected = [
        Node(
            content=MacroNodeContent(
                "macroname",
                unnamed_args=[],
                named_args={},
            ),
            info=NodeInfo(context=generate_context(0, 0, 0, 13)),
        )
    ]

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        expected,
    )
