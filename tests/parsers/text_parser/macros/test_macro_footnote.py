import pytest

from mau.lexers.text_lexer import TextLexer
from mau.nodes.footnote import FootnoteNode
from mau.nodes.macro import MacroFootnoteNode
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


def test_macro_footnote():
    source = "[footnote](notename)"

    footnote_node = FootnoteNode(name="notename")

    footnote_macro_node = MacroFootnoteNode(
        footnote=footnote_node,
        info=NodeInfo(context=generate_context(0, 0, 0, 20)),
    )

    parser = runner(source)

    compare_nodes_sequence(parser.nodes, [footnote_macro_node])
    compare_nodes_sequence(parser.footnotes, [footnote_node])


def test_macro_footnote_without_name():
    source = "[footnote]()"

    with pytest.raises(MauParserException) as exc:
        runner(source)

    assert exc.value.context == generate_context(0, 0, 0, 12)
