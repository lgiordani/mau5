from mau.lexers.text_lexer import TextLexer
from mau.nodes.inline import StyleNodeContent, TextNodeContent
from mau.nodes.macros import MacroLinkNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.text_parser import TextParser
from mau.test_helpers import (
    init_parser_factory,
    parser_runner_factory,
    generate_context,
)

init_parser = init_parser_factory(TextLexer, TextParser)

runner = parser_runner_factory(TextLexer, TextParser)


def test_macro_link():
    source = '[link](https://somedomain.org/the/path, "link text")'

    expected = [
        Node(
            children=[
                Node(
                    content=TextNodeContent("link text"),
                    info=NodeInfo(context=generate_context(0, 40)),
                )
            ],
            content=MacroLinkNodeContent(
                "https://somedomain.org/the/path",
            ),
            info=NodeInfo(context=generate_context(0, 0)),
        ),
    ]

    assert runner(source).nodes == expected


def test_macro_link_without_text():
    source = '[link]("https://somedomain.org/the/path")'

    expected = [
        Node(
            children=[
                Node(
                    content=TextNodeContent("https://somedomain.org/the/path"),
                    info=NodeInfo(context=generate_context(0, 8)),
                )
            ],
            content=MacroLinkNodeContent(
                "https://somedomain.org/the/path",
            ),
        ),
    ]

    assert runner(source).nodes == expected


def test_macro_link_with_rich_text():
    source = (
        '[link]("https://somedomain.org/the/path", "Some text with _styled words_")'
    )

    expected = [
        Node(
            children=[
                Node(
                    content=TextNodeContent("Some text with "),
                    info=NodeInfo(context=generate_context(0, 38)),
                ),
                Node(
                    children=[
                        Node(
                            content=TextNodeContent("styled words"),
                            info=NodeInfo(context=generate_context(0, 54)),
                        ),
                    ],
                    content=StyleNodeContent("underscore"),
                    info=NodeInfo(context=generate_context(0, 53)),
                ),
            ],
            content=MacroLinkNodeContent(
                "https://somedomain.org/the/path",
            ),
            info=NodeInfo(context=generate_context(0, 0)),
        ),
    ]

    assert runner(source).nodes == expected


def test_macro_mailto():
    source = "[mailto](info@projectmau.org)"

    expected = [
        Node(
            children=[
                Node(
                    content=TextNodeContent("info@projectmau.org"),
                    info=NodeInfo(context=generate_context(0, 9)),
                ),
            ],
            content=MacroLinkNodeContent(
                "mailto:info@projectmau.org",
            ),
            info=NodeInfo(context=generate_context(0, 9)),
        ),
    ]

    assert runner(source).nodes == expected


def test_macro_mailto_custom_text():
    source = '[mailto](info@projectmau.org, "my email")'

    expected = [
        Node(
            children=[
                Node(
                    content=TextNodeContent("my email"),
                    info=NodeInfo(context=generate_context(0, 31)),
                ),
            ],
            content=MacroLinkNodeContent(
                "mailto:info@projectmau.org",
            ),
            info=NodeInfo(context=generate_context(0, 9)),
        ),
    ]

    assert runner(source).nodes == expected
