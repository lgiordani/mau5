import pytest

from mau.lexers.text_lexer import TextLexer
from mau.nodes.footnotes import FootnoteNodeContent
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


def test_macro_footnote():
    source = "[footnote](notename)"

    footnote_node = Node(
        content=FootnoteNodeContent(),
        info=NodeInfo(context=generate_context(0, 0)),
    )
    expected = [footnote_node]

    parser = runner(source)
    assert parser.nodes == expected
    assert parser.footnotes == {"notename": footnote_node}


def test_macro_footnote_without_name():
    source = "[footnote]()"

    with pytest.raises(MauParserException) as exc:
        runner(source)

    assert exc.value.context == generate_context(0, 0)
