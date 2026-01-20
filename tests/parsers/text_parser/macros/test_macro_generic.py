from mau.lexers.text_lexer import TextLexer
from mau.nodes.inline import TextNode
from mau.nodes.macro import MacroNode
from mau.nodes.node import NodeInfo
from mau.parsers.text_parser import TextParser
from mau.test_helpers import (
    compare_nodes_sequence,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(TextLexer, TextParser)

runner = parser_runner_factory(TextLexer, TextParser)


def test_generic_macro():
    source = "[macroname](value1,value2)"

    expected = [
        MacroNode(
            "macroname",
            unnamed_args=["value1", "value2"],
            info=NodeInfo(context=generate_context(0, 0, 0, 26)),
        )
    ]

    compare_nodes_sequence(runner(source).nodes, expected)


def test_generic_macro_incomplete():
    source = "[macroname](value1"

    expected = [
        TextNode(
            "[macroname](value1",
            info=NodeInfo(context=generate_context(0, 0, 0, 18)),
        ),
    ]

    compare_nodes_sequence(runner(source).nodes, expected)


def test_generic_macro_named_arguments():
    source = "[macroname](name,arg1=value1)"

    expected = [
        MacroNode(
            "macroname",
            unnamed_args=["name"],
            named_args={"arg1": "value1"},
            info=NodeInfo(context=generate_context(0, 0, 0, 29)),
        )
    ]

    compare_nodes_sequence(runner(source).nodes, expected)


def test_generic_macro_without_arguments():
    source = "[macroname]()"

    expected = [
        MacroNode(
            "macroname",
            unnamed_args=[],
            named_args={},
            info=NodeInfo(context=generate_context(0, 0, 0, 13)),
        )
    ]

    compare_nodes_sequence(runner(source).nodes, expected)
