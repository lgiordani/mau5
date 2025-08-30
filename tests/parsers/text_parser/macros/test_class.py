from mau.lexers.text_lexer import TextLexer
from mau.nodes.inline import StyleNodeContent, TextNodeContent, VerbatimNodeContent
from mau.nodes.macros import MacroClassNodeContent
from mau.nodes.node import Node
from mau.parsers.text_parser import TextParser
from mau.test_helpers import init_parser_factory, parser_runner_factory

init_parser = init_parser_factory(TextLexer, TextParser)

runner = parser_runner_factory(TextLexer, TextParser)


def test_single_class():
    source = 'Some text [class]("text with that class", classname)'

    expected = [
        Node(content=TextNodeContent("Some text ")),
        Node(
            children=[Node(content=TextNodeContent("text with that class"))],
            content=MacroClassNodeContent(classes=["classname"]),
        ),
    ]

    assert runner(source).nodes == expected


def test_multiple_classes():
    source = 'Some text [class]("text with that class", classname1, classname2)'

    expected = [
        Node(content=TextNodeContent("Some text ")),
        Node(
            children=[Node(content=TextNodeContent("text with that class"))],
            content=MacroClassNodeContent(classes=["classname1", "classname2"]),
        ),
    ]

    assert runner(source).nodes == expected


def test_parse_class_with_rich_text():
    source = '[class]("Some text with `verbatim words` and _styled ones_", classname)'

    macro_node = Node(
        children=[
            Node(content=TextNodeContent("Some text with ")),
            Node(content=VerbatimNodeContent("verbatim words")),
            Node(content=TextNodeContent(" and ")),
            Node(
                children=[Node(content=TextNodeContent("styled ones"))],
                content=StyleNodeContent("underscore"),
            ),
        ],
        content=MacroClassNodeContent(classes=["classname"]),
    )

    expected = [macro_node]

    assert runner(source).nodes == expected
