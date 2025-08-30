import pytest

from mau.environment.environment import Environment
from mau.lexers.text_lexer import TextLexer
from mau.nodes.inline import SentenceNodeContent, StyleNodeContent, TextNodeContent
from mau.nodes.node import Node
from mau.parsers.base_parser import MauParserException
from mau.parsers.text_parser import TextParser
from mau.test_helpers import init_parser_factory, parser_runner_factory

init_parser = init_parser_factory(TextLexer, TextParser)

runner = parser_runner_factory(TextLexer, TextParser)


def test_control_if_true():
    environment = Environment.from_dict({"flag": True})

    source = '[@if](flag, &true, "TRUE", "FALSE")'

    sentence_node = Node(
        children=[Node(content=TextNodeContent("TRUE"))], content=SentenceNodeContent()
    )

    expected = [sentence_node]

    assert runner(source, environment=environment).nodes == expected


def test_control_if_false():
    environment = Environment.from_dict({"flag": True})

    source = '[@if](flag, &false, "TRUE", "FALSE")'

    expected = [
        Node(
            children=[Node(content=TextNodeContent("FALSE"))],
            content=SentenceNodeContent(),
        ),
    ]

    nodes = runner(source, environment=environment).nodes

    assert nodes == expected


def test_control_if_equal():
    environment = Environment.from_dict({"flag": "42"})

    source = '[@if](flag, "=42", "TRUE", "FALSE")'

    expected = [
        Node(
            children=[Node(content=TextNodeContent("TRUE"))],
            content=SentenceNodeContent(),
        ),
    ]

    assert runner(source, environment=environment).nodes == expected


def test_control_if_not_equal():
    environment = Environment.from_dict({"flag": "42"})

    source = '[@if](flag, "!=42", TRUE", "FALSE")'

    expected = [
        Node(
            children=[Node(content=TextNodeContent("FALSE"))],
            content=SentenceNodeContent(),
        ),
    ]

    assert runner(source, environment=environment).nodes == expected


def test_control_wrong_name_format():
    environment = Environment.from_dict({"flag": "42"})

    source = '[@if](flag, "TRUE", "FALSE")'

    with pytest.raises(MauParserException):
        runner(source, environment=environment)


def test_control_unsupported_operator():
    environment = Environment.from_dict({"flag": "42"})

    source = '[@something](flag, &true, "TRUE", "FALSE")'

    with pytest.raises(MauParserException):
        runner(source, environment=environment)


def test_control_undefined_variable():
    source = '[@if](flag, &true, "TRUE", "FALSE")'

    with pytest.raises(MauParserException):
        runner(source)


def test_control_invalid_boolean():
    environment = Environment.from_dict({"flag": "42"})

    source = '[@if](flag, &something, "TRUE", "FALSE")'

    with pytest.raises(MauParserException):
        runner(source, environment)


def test_control_invalid_test():
    environment = Environment.from_dict({"flag": "42"})

    source = '[@if](flag, -something, "TRUE", "FALSE")'

    with pytest.raises(MauParserException):
        runner(source, environment)


def test_macro_ifeval_true():
    environment = Environment.from_dict(
        {
            "flag": True,
            "underscore": "_sometext_",
            "star": "*othertext*",
        }
    )

    source = "[@ifeval](flag, &true, underscore, star)"

    expected = [
        Node(
            children=[
                Node(
                    children=[
                        Node(content=TextNodeContent("sometext")),
                    ],
                    content=StyleNodeContent("underscore"),
                )
            ],
            content=SentenceNodeContent(),
        ),
    ]

    assert runner(source, environment=environment).nodes == expected


def test_macro_ifeval_false():
    environment = Environment.from_dict(
        {
            "flag": True,
            "underscore": "_sometext_",
            "star": "*othertext*",
        }
    )

    source = "[@ifeval](flag, &false, underscore, star)"

    expected = [
        Node(
            children=[
                Node(
                    children=[
                        Node(content=TextNodeContent("othertext")),
                    ],
                    content=StyleNodeContent("star"),
                )
            ],
            content=SentenceNodeContent(),
        ),
    ]

    assert runner(source, environment=environment).nodes == expected


def test_macro_ifeval_false_is_not_evaluated():
    environment = Environment.from_dict(
        {
            "flag": True,
            "style": "_sometext_",
            "header": "[header](notexists)",
        }
    )

    source = "[@ifeval](flag, &true, style, header)"

    expected = [
        Node(
            children=[
                Node(
                    children=[
                        Node(content=TextNodeContent("sometext")),
                    ],
                    content=StyleNodeContent("underscore"),
                )
            ],
            content=SentenceNodeContent(),
        ),
    ]

    assert runner(source, environment=environment).nodes == expected


def test_macro_ifeval_true_is_not_evaluated():
    environment = Environment.from_dict(
        {
            "flag": True,
            "style": "_sometext_",
            "header": "[header](notexists)",
        }
    )

    source = "[@ifeval](flag, &false, header, style)"

    expected = [
        Node(
            children=[
                Node(
                    children=[
                        Node(content=TextNodeContent("sometext")),
                    ],
                    content=StyleNodeContent("underscore"),
                )
            ],
            content=SentenceNodeContent(),
        ),
    ]

    assert runner(source, environment=environment).nodes == expected


def test_macro_ifeval_true_not_defined():
    environment = Environment.from_dict(
        {
            "flag": True,
            "star": "*othertext*",
        }
    )

    source = "[@ifeval](flag, &true, underscore, star)"

    with pytest.raises(MauParserException):
        runner(source, environment)


def test_macro_ifeval_false_not_defined():
    environment = Environment.from_dict(
        {
            "flag": True,
            "underscore": "_sometext_",
        }
    )

    source = "[@ifeval](flag, &false, underscore, star)"

    with pytest.raises(MauParserException):
        runner(source, environment)
