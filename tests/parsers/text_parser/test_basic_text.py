from mau.lexers.text_lexer import TextLexer
from mau.nodes.inline import TextNodeData
from mau.nodes.node import Node, NodeInfo
from mau.parsers.text_parser import TextParser
from mau.test_helpers import (
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(TextLexer, TextParser)

runner = parser_runner_factory(TextLexer, TextParser)


def test_empty_text():
    source = ""

    assert runner(source).nodes == []


def test_parse_word():
    source = "Word"

    expected = [
        Node(
            data=TextNodeData("Word"),
            info=NodeInfo(context=generate_context(0, 0, 0, 4)),
        ),
    ]

    assert runner(source).nodes == expected


def test_multiple_words():
    source = "Many different words"

    expected = [
        Node(
            data=TextNodeData("Many different words"),
            info=NodeInfo(context=generate_context(0, 0, 0, 20)),
        ),
    ]

    assert runner(source).nodes == expected


def test_parse_escape_word():
    source = r"\Escaped"

    expected = [
        Node(
            data=TextNodeData("Escaped"),
            info=NodeInfo(context=generate_context(0, 0, 0, 8)),
        ),
    ]

    assert runner(source).nodes == expected


def test_parse_escape_symbol():
    source = r"\"Escaped"

    expected = [
        Node(
            data=TextNodeData('"Escaped'),
            info=NodeInfo(context=generate_context(0, 0, 0, 9)),
        ),
    ]

    assert runner(source).nodes == expected


def test_square_brackets():
    source = "This contains [ and ] and [this]"

    expected = [
        Node(
            data=TextNodeData("This contains [ and ] and [this]"),
            info=NodeInfo(context=generate_context(0, 0, 0, 32)),
        ),
    ]

    assert runner(source).nodes == expected
