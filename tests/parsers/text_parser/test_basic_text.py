from mau.lexers.text_lexer import TextLexer
from mau.nodes.inline import TextNodeContent
from mau.nodes.node import Node
from mau.parsers.text_parser import TextParser
from mau.test_helpers import init_parser_factory, parser_runner_factory

init_parser = init_parser_factory(TextLexer, TextParser)

runner = parser_runner_factory(TextLexer, TextParser)


def test_empty_text():
    source = ""

    assert runner(source).nodes == []


def test_parse_word():
    source = "Word"

    expected = [
        Node(content=TextNodeContent("Word")),
    ]

    assert runner(source).nodes == expected


def test_multiple_words():
    source = "Many different words"

    expected = [
        Node(content=TextNodeContent("Many different words")),
    ]

    assert runner(source).nodes == expected


def test_parse_escape_word():
    source = r"\Escaped"

    expected = [
        Node(content=TextNodeContent("Escaped")),
    ]

    assert runner(source).nodes == expected


def test_parse_escape_symbol():
    source = r"\"Escaped"

    expected = [
        Node(content=TextNodeContent('"Escaped')),
    ]

    assert runner(source).nodes == expected


def test_square_brackets():
    source = "This contains [ and ] and [this]"

    expected = [
        Node(content=TextNodeContent("This contains [ and ] and [this]")),
    ]

    assert runner(source).nodes == expected
