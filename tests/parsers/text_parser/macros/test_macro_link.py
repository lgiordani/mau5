import pytest

from mau.lexers.text_lexer import TextLexer
from mau.nodes.inline import StyleNodeData, TextNodeData
from mau.nodes.macros import MacroLinkNodeData
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


def test_macro_link():
    source = '[link](https://somedomain.org/the/path, "link text")'

    expected = [
        Node(
            data=MacroLinkNodeData(
                "https://somedomain.org/the/path",
                content=[
                    Node(
                        data=TextNodeData("link text"),
                        info=NodeInfo(context=generate_context(0, 41, 0, 50)),
                    )
                ],
            ),
            info=NodeInfo(context=generate_context(0, 0, 0, 52)),
        ),
    ]

    assert runner(source).nodes == expected


def test_macro_link_without_text():
    source = '[link]("https://somedomain.org/the/path")'

    expected = [
        Node(
            data=MacroLinkNodeData(
                "https://somedomain.org/the/path",
                content=[
                    Node(
                        data=TextNodeData("https://somedomain.org/the/path"),
                        info=NodeInfo(context=generate_context(0, 8, 0, 39)),
                    )
                ],
            ),
            info=NodeInfo(context=generate_context(0, 0, 0, 41)),
        ),
    ]

    assert runner(source).nodes == expected


def test_macro_link_without_target():
    source = "[link]()"

    with pytest.raises(MauParserException) as exc:
        runner(source)

    assert exc.value.context == generate_context(0, 0, 0, 8)


def test_macro_link_with_rich_text():
    source = (
        '[link]("https://somedomain.org/the/path", "Some text with _styled words_")'
    )

    expected = [
        Node(
            data=MacroLinkNodeData(
                "https://somedomain.org/the/path",
                content=[
                    Node(
                        data=TextNodeData("Some text with "),
                        info=NodeInfo(context=generate_context(0, 43, 0, 58)),
                    ),
                    Node(
                        data=StyleNodeData(
                            "underscore",
                            content=[
                                Node(
                                    data=TextNodeData("styled words"),
                                    info=NodeInfo(
                                        context=generate_context(0, 59, 0, 71)
                                    ),
                                ),
                            ],
                        ),
                        info=NodeInfo(context=generate_context(0, 58, 0, 72)),
                    ),
                ],
            ),
            info=NodeInfo(context=generate_context(0, 0, 0, 74)),
        ),
    ]

    assert runner(source).nodes == expected


def test_macro_mailto():
    source = "[mailto](info@projectmau.org)"

    expected = [
        Node(
            data=MacroLinkNodeData(
                "mailto:info@projectmau.org",
                content=[
                    Node(
                        data=TextNodeData("info@projectmau.org"),
                        info=NodeInfo(context=generate_context(0, 9, 0, 28)),
                    ),
                ],
            ),
            info=NodeInfo(context=generate_context(0, 0, 0, 29)),
        ),
    ]

    assert runner(source).nodes == expected


def test_macro_mailto_custom_text():
    source = '[mailto](info@projectmau.org, "my email")'

    expected = [
        Node(
            data=MacroLinkNodeData(
                "mailto:info@projectmau.org",
                content=[
                    Node(
                        data=TextNodeData("my email"),
                        info=NodeInfo(context=generate_context(0, 31, 0, 39)),
                    ),
                ],
            ),
            info=NodeInfo(context=generate_context(0, 0, 0, 41)),
        ),
    ]

    assert runner(source).nodes == expected


def test_macro_mailto_without_target():
    source = "[mailto]()"

    with pytest.raises(MauParserException) as exc:
        runner(source)

    assert exc.value.context == generate_context(0, 0, 0, 10)
