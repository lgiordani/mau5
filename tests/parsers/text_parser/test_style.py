from mau.lexers.text_lexer.lexer import TextLexer
from mau.nodes.inline import StyleNodeContent, TextNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.text_parser.parser import TextParser
from mau.test_helpers import (
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(TextLexer, TextParser)

runner = parser_runner_factory(TextLexer, TextParser)


def test_underscore():
    source = "_Some text_"

    expected_node = Node(
        children={
            "content": [
                Node(
                    content=TextNodeContent("Some text"),
                    info=NodeInfo(context=generate_context(0, 1, 0, 10)),
                )
            ]
        },
        content=StyleNodeContent("underscore"),
        info=NodeInfo(context=generate_context(0, 0, 0, 11)),
    )

    assert runner(source).nodes == [expected_node]


def test_star():
    source = "*Some text*"

    expected_node = Node(
        children={
            "content": [
                Node(
                    content=TextNodeContent("Some text"),
                    info=NodeInfo(context=generate_context(0, 1, 0, 10)),
                )
            ]
        },
        content=StyleNodeContent("star"),
        info=NodeInfo(context=generate_context(0, 0, 0, 11)),
    )

    assert runner(source).nodes == [expected_node]


def test_caret():
    source = "^Some text^"

    expected_node = Node(
        children={
            "content": [
                Node(
                    content=TextNodeContent("Some text"),
                    info=NodeInfo(context=generate_context(0, 1, 0, 10)),
                )
            ]
        },
        content=StyleNodeContent("caret"),
        info=NodeInfo(context=generate_context(0, 0, 0, 11)),
    )

    assert runner(source).nodes == [expected_node]


def test_tilde():
    source = "~Some text~"

    expected_node = Node(
        children={
            "content": [
                Node(
                    content=TextNodeContent("Some text"),
                    info=NodeInfo(context=generate_context(0, 1, 0, 10)),
                )
            ]
        },
        content=StyleNodeContent("tilde"),
        info=NodeInfo(context=generate_context(0, 0, 0, 11)),
    )

    assert runner(source).nodes == [expected_node]


def test_style_within_style():
    source = "_*Words with two styles*_"

    expected_node = Node(
        content=StyleNodeContent("underscore"),
        info=NodeInfo(context=generate_context(0, 0, 0, 25)),
        children={
            "content": [
                Node(
                    content=StyleNodeContent("star"),
                    info=NodeInfo(context=generate_context(0, 1, 0, 24)),
                    children={
                        "content": [
                            Node(
                                content=TextNodeContent("Words with two styles"),
                                info=NodeInfo(context=generate_context(0, 2, 0, 23)),
                            )
                        ]
                    },
                )
            ]
        },
    )

    assert runner(source).nodes == [expected_node]


def test_double_style_cancels_itself():
    source = "__Text__"

    expected = [
        Node(
            content=StyleNodeContent("underscore"),
            info=NodeInfo(context=generate_context(0, 0, 0, 2)),
        ),
        Node(
            content=TextNodeContent("Text"),
            info=NodeInfo(context=generate_context(0, 2, 0, 6)),
        ),
        Node(
            content=StyleNodeContent("underscore"),
            info=NodeInfo(context=generate_context(0, 6, 0, 8)),
        ),
    ]

    assert runner(source).nodes == expected


def test_mix_text_and_styles():
    source = "Some text _and style_ and *more style* here"

    expected = [
        Node(
            content=TextNodeContent("Some text "),
            info=NodeInfo(context=generate_context(0, 0, 0, 10)),
        ),
        Node(
            children={
                "content": [
                    Node(
                        content=TextNodeContent("and style"),
                        info=NodeInfo(context=generate_context(0, 11, 0, 20)),
                    )
                ]
            },
            content=StyleNodeContent("underscore"),
            info=NodeInfo(context=generate_context(0, 10, 0, 21)),
        ),
        Node(
            content=TextNodeContent(" and "),
            info=NodeInfo(context=generate_context(0, 21, 0, 26)),
        ),
        Node(
            children={
                "content": [
                    Node(
                        content=TextNodeContent("more style"),
                        info=NodeInfo(context=generate_context(0, 27, 0, 37)),
                    )
                ]
            },
            content=StyleNodeContent("star"),
            info=NodeInfo(context=generate_context(0, 26, 0, 38)),
        ),
        Node(
            content=TextNodeContent(" here"),
            info=NodeInfo(context=generate_context(0, 38, 0, 43)),
        ),
    ]

    assert runner(source).nodes == expected


def test_unclosed_style():
    source = "_Text"

    expected = [
        Node(
            content=TextNodeContent("_Text"),
            info=NodeInfo(context=generate_context(0, 0, 0, 5)),
        ),
    ]

    assert runner(source).nodes == expected
