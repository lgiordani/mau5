import pytest

from mau.lexers.text_lexer import TextLexer
from mau.nodes.inline import TextNodeData
from mau.nodes.macros import MacroHeaderNodeData
from mau.nodes.node import Node, NodeInfo
from mau.parsers.base_parser import MauParserException
from mau.parsers.text_parser import TextParser
from mau.test_helpers import (
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(TextLexer, TextParser)

runner = parser_runner_factory(TextLexer, TextParser)


def test_macro_header():
    source = '[header](id, "link text")'

    expected_node = Node(
        data=MacroHeaderNodeData(
            "id",
            content=[
                Node(
                    data=TextNodeData("link text"),
                    info=NodeInfo(context=generate_context(0, 14, 0, 23)),
                )
            ],
        ),
        info=NodeInfo(context=generate_context(0, 0, 0, 25)),
    )

    parser = runner(source)
    assert parser.nodes == [expected_node]
    assert parser.header_links == [expected_node]


def test_macro_header_without_text():
    source = "[header](id)"

    expected_node = Node(
        data=MacroHeaderNodeData(
            "id",
        ),
        info=NodeInfo(context=generate_context(0, 0, 0, 12)),
    )

    parser = runner(source)
    assert parser.nodes == [expected_node]
    assert parser.header_links == [expected_node]


def test_macro_header_without_target():
    source = "[header]()"

    with pytest.raises(MauParserException) as exc:
        runner(source)

    assert exc.value.context == generate_context(0, 0, 0, 10)
