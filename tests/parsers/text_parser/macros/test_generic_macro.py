from mau.lexers.text_lexer import TextLexer
from mau.nodes.inline import TextNodeContent
from mau.nodes.macros import MacroNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.text_parser import TextParser
from mau.test_helpers import init_parser_factory, parser_runner_factory

init_parser = init_parser_factory(TextLexer, TextParser)

runner = parser_runner_factory(TextLexer, TextParser)


def test_macro():
    source = "[macroname](value1,value2)"

    expected = [
        Node(
            content=MacroNodeContent("macroname"),
            info=NodeInfo(unnamed_args=["value1", "value2"]),
        )
    ]

    assert runner(source).nodes == expected


def test_incomplete_macro():
    source = "[macroname](value1"

    expected = [
        Node(
            content=TextNodeContent(
                "[macroname](value1",
            )
        ),
    ]

    assert runner(source).nodes == expected


def test_macro_arguments_with_quotes():
    source = '[macroname]("value1,value2")'

    expected = [
        Node(
            content=MacroNodeContent("macroname"),
            info=NodeInfo(unnamed_args=["value1,value2"]),
        )
    ]

    assert runner(source).nodes == expected


def test_macro_named_arguments():
    source = "[macroname](name,arg1=value1)"

    expected = [
        Node(
            content=MacroNodeContent("macroname"),
            info=NodeInfo(
                unnamed_args=["name"],
                named_args={"arg1": "value1"},
            ),
        )
    ]

    assert runner(source).nodes == expected
