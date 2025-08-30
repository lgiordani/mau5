from mau.lexers.text_lexer import TextLexer
from mau.nodes.footnotes import FootnoteNodeContent
from mau.nodes.node import Node
from mau.parsers.text_parser import TextParser
from mau.test_helpers import init_parser_factory, parser_runner_factory

init_parser = init_parser_factory(TextLexer, TextParser)

runner = parser_runner_factory(TextLexer, TextParser)


def test_macro_footnote():
    source = "[footnote](notename)"

    footnote_node = Node(content=FootnoteNodeContent())
    expected = [footnote_node]

    parser = runner(source)
    assert parser.nodes == expected
    assert parser.footnotes == {"notename": footnote_node}
