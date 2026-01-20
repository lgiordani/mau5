import pytest

from mau.lexers.text_lexer import TextLexer
from mau.nodes.inline import TextNode
from mau.nodes.macro import MacroHeaderNode
from mau.nodes.node import NodeInfo
from mau.parsers.base_parser import MauParserException
from mau.parsers.text_parser import TextParser
from mau.test_helpers import (
    compare_nodes_sequence,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(TextLexer, TextParser)

runner = parser_runner_factory(TextLexer, TextParser)


def test_macro_header():
    source = '[header](id, "link text")'

    expected = [
        MacroHeaderNode(
            "id",
            content=[
                TextNode(
                    "link text",
                    info=NodeInfo(context=generate_context(0, 14, 0, 23)),
                )
            ],
            info=NodeInfo(context=generate_context(0, 0, 0, 25)),
        )
    ]

    parser = runner(source)

    compare_nodes_sequence(parser.nodes, expected)
    compare_nodes_sequence(parser.header_links, expected)


def test_macro_header_without_text():
    source = "[header](id)"

    expected = [
        MacroHeaderNode(
            "id",
            info=NodeInfo(context=generate_context(0, 0, 0, 12)),
        )
    ]

    parser = runner(source)

    compare_nodes_sequence(parser.nodes, expected)
    compare_nodes_sequence(parser.header_links, expected)


def test_macro_header_without_target():
    source = "[header]()"

    with pytest.raises(MauParserException) as exc:
        runner(source)

    assert exc.value.context == generate_context(0, 0, 0, 10)
