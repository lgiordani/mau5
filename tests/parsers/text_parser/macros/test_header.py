from mau.lexers.text_lexer import TextLexer
from mau.nodes.inline import TextNodeContent
from mau.nodes.macros import MacroHeaderNodeContent
from mau.nodes.node import Node
from mau.parsers.text_parser import TextParser
from mau.test_helpers import init_parser_factory, parser_runner_factory

init_parser = init_parser_factory(TextLexer, TextParser)

runner = parser_runner_factory(TextLexer, TextParser)


def test_macro_header():
    source = '[header](id, "link text")'

    node = Node(
        children=[Node(content=TextNodeContent("link text"))],
        content=MacroHeaderNodeContent("id"),
    )
    parser = runner(source)
    assert parser.nodes == [node]
    assert parser.header_links == [node]


def test_macro_header_without_text():
    source = "[header](id)"

    node = Node(content=MacroHeaderNodeContent("id"))

    parser = runner(source)
    assert parser.nodes == [node]
    assert parser.header_links == [node]
