import pytest

from mau.lexers.text_lexer import TextLexer
from mau.nodes.inline import StyleNodeContent, TextNodeContent, VerbatimNodeContent
from mau.nodes.macros import MacroClassNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.base_parser import MauParserException
from mau.parsers.text_parser import TextParser
from mau.test_helpers import (
    compare_nodes,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(TextLexer, TextParser)

runner = parser_runner_factory(TextLexer, TextParser)


def test_macro_class_with_single_class():
    source = '[class]("text with that class", classname)'

    expected_nodes = [
        Node(
            children={
                "text": [
                    Node(
                        content=TextNodeContent("text with that class"),
                        info=NodeInfo(context=generate_context(0, 9, 0, 29)),
                    )
                ]
            },
            content=MacroClassNodeContent(["classname"]),
            info=NodeInfo(context=generate_context(0, 0, 0, 42)),
        ),
    ]

    parser = runner(source)

    compare_nodes(parser.nodes, expected_nodes)


def test_macro_class_with_multiple_classes():
    source = '[class]("text with that class", classname1, classname2)'

    expected_nodes = [
        Node(
            children={
                "text": [
                    Node(
                        content=TextNodeContent("text with that class"),
                        info=NodeInfo(context=generate_context(0, 9, 0, 29)),
                    )
                ]
            },
            content=MacroClassNodeContent(["classname1", "classname2"]),
            info=NodeInfo(context=generate_context(0, 0, 0, 55)),
        ),
    ]

    parser = runner(source)

    compare_nodes(parser.nodes, expected_nodes)


def test_macro_class_with_rich_text():
    source = '[class]("Some text with `verbatim words` and _styled ones_", classname)'

    expected_nodes = [
        Node(
            children={
                "text": [
                    Node(
                        content=TextNodeContent("Some text with "),
                        info=NodeInfo(context=generate_context(0, 9, 0, 24)),
                    ),
                    Node(
                        content=VerbatimNodeContent("verbatim words"),
                        info=NodeInfo(context=generate_context(0, 24, 0, 40)),
                    ),
                    Node(
                        content=TextNodeContent(" and "),
                        info=NodeInfo(context=generate_context(0, 40, 0, 45)),
                    ),
                    Node(
                        children={
                            "content": [
                                Node(
                                    content=TextNodeContent("styled ones"),
                                    info=NodeInfo(
                                        context=generate_context(0, 46, 0, 57)
                                    ),
                                )
                            ]
                        },
                        content=StyleNodeContent("underscore"),
                        info=NodeInfo(context=generate_context(0, 45, 0, 58)),
                    ),
                ]
            },
            content=MacroClassNodeContent(["classname"]),
            info=NodeInfo(context=generate_context(0, 0, 0, 71)),
        ),
    ]

    parser = runner(source)

    compare_nodes(parser.nodes, expected_nodes)


def test_macro_class_without_classes():
    source = '[class]("text with that class")'

    expected_nodes = [
        Node(
            children={
                "text": [
                    Node(
                        content=TextNodeContent("text with that class"),
                        info=NodeInfo(context=generate_context(0, 9, 0, 29)),
                    )
                ]
            },
            content=MacroClassNodeContent([]),
            info=NodeInfo(context=generate_context(0, 0, 0, 31)),
        ),
    ]

    parser = runner(source)

    compare_nodes(parser.nodes, expected_nodes)


def test_macro_class_without_text():
    source = "[class]()"

    with pytest.raises(MauParserException) as exc:
        runner(source)

    assert exc.value.context == generate_context(0, 0, 0, 9)
