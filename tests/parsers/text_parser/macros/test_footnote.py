import pytest

from mau.lexers.text_lexer.lexer import TextLexer
from mau.nodes.macros import MacroFootnoteNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.base_parser.parser import MauParserException
from mau.parsers.text_parser.parser import TextParser
from mau.test_helpers import (
    compare_nodes,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(TextLexer, TextParser)

runner = parser_runner_factory(TextLexer, TextParser)


def test_macro_footnote():
    source = "[footnote](notename)"

    footnote_node = Node(
        content=MacroFootnoteNodeContent("notename"),
        info=NodeInfo(context=generate_context(0, 0, 0, 20)),
    )

    parser = runner(source)

    compare_nodes(parser.nodes, [footnote_node])

    assert parser.footnotes == [footnote_node]


def test_macro_footnote_without_name():
    source = "[footnote]()"

    with pytest.raises(MauParserException) as exc:
        runner(source)

    assert exc.value.context == generate_context(0, 0, 0, 12)
