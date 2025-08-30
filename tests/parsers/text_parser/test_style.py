from mau.lexers.text_lexer import TextLexer
from mau.nodes.inline import StyleNodeContent, TextNodeContent
from mau.nodes.node import Node
from mau.parsers.text_parser import TextParser
from mau.test_helpers import init_parser_factory, parser_runner_factory

init_parser = init_parser_factory(TextLexer, TextParser)

runner = parser_runner_factory(TextLexer, TextParser)


def test_underscore():
    source = "_Some text_"

    expected_node = Node(
        children=[Node(content=TextNodeContent("Some text"))],
        content=StyleNodeContent("underscore"),
    )

    assert runner(source).nodes == [expected_node]


def test_star():
    source = "*Some text*"

    expected_node = Node(
        children=[Node(content=TextNodeContent("Some text"))],
        content=StyleNodeContent("star"),
    )

    assert runner(source).nodes == [expected_node]


def test_caret():
    source = "^Some text^"

    expected_node = Node(
        children=[Node(content=TextNodeContent("Some text"))],
        content=StyleNodeContent("caret"),
    )

    assert runner(source).nodes == [expected_node]


def test_tilde():
    source = "~Some text~"

    expected_node = Node(
        children=[Node(content=TextNodeContent("Some text"))],
        content=StyleNodeContent("tilde"),
    )

    assert runner(source).nodes == [expected_node]


def test_style_within_style():
    source = "_*Words with two styles*_"

    star_node = Node(
        children=[Node(content=TextNodeContent("Words with two styles"))],
        content=StyleNodeContent("star"),
    )

    underscore_node = Node(content=StyleNodeContent("underscore"))
    underscore_node.add_children([star_node])

    assert runner(source).nodes == [underscore_node]


def test_double_style_cancels_itself():
    source = "__Text__"

    expected = [
        Node(content=StyleNodeContent("underscore")),
        Node(content=TextNodeContent("Text")),
        Node(content=StyleNodeContent("underscore")),
    ]

    assert runner(source).nodes == expected


def test_mix_text_and_styles():
    source = "Some text _and style_ and *more style* here"

    expected = [
        Node(content=TextNodeContent("Some text ")),
        Node(
            children=[Node(content=TextNodeContent("and style"))],
            content=StyleNodeContent("underscore"),
        ),
        Node(content=TextNodeContent(" and ")),
        Node(
            children=[Node(content=TextNodeContent("more style"))],
            content=StyleNodeContent("star"),
        ),
        Node(content=TextNodeContent(" here")),
    ]

    assert runner(source).nodes == expected


def test_unclosed_style():
    source = "_Text"

    expected = [
        Node(content=TextNodeContent("_Text")),
    ]

    assert runner(source).nodes == expected
