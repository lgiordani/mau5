import pytest

from mau.environment.environment import Environment
from mau.lexers.text_lexer.lexer import TextLexer
from mau.nodes.inline import SentenceNodeContent, StyleNodeContent, TextNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.base_parser.parser import MauParserException
from mau.parsers.text_parser.parser import TextParser
from mau.test_helpers import (
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(TextLexer, TextParser)

runner = parser_runner_factory(TextLexer, TextParser)


def test_macro_control_if_true():
    environment = Environment.from_dict({"flag": True})

    source = '[@if](flag, &true, "TRUE", "FALSE")'

    sentence_node = Node(
        children={
            "content": [
                Node(
                    content=TextNodeContent("TRUE"),
                    info=NodeInfo(context=generate_context(0, 20)),
                )
            ]
        },
        content=SentenceNodeContent(),
        info=NodeInfo(context=generate_context(0, 0)),
    )

    expected = [sentence_node]

    assert runner(source, environment=environment).nodes == expected


def test_macro_control_if_false():
    environment = Environment.from_dict({"flag": True})

    source = '[@if](flag, &false, "TRUE", "FALSE")'

    expected = [
        Node(
            children={
                "content": [
                    Node(
                        content=TextNodeContent("FALSE"),
                        info=NodeInfo(context=generate_context(0, 29)),
                    )
                ]
            },
            content=SentenceNodeContent(),
            info=NodeInfo(context=generate_context(0, 0)),
        ),
    ]

    nodes = runner(source, environment=environment).nodes

    assert nodes == expected


def test_macro_control_if_equal():
    environment = Environment.from_dict({"flag": "42"})

    source = '[@if](flag, "=42", "TRUE", "FALSE")'

    expected = [
        Node(
            children={
                "content": [
                    Node(
                        content=TextNodeContent("TRUE"),
                        info=NodeInfo(context=generate_context(0, 20)),
                    )
                ]
            },
            content=SentenceNodeContent(),
            info=NodeInfo(context=generate_context(0, 0)),
        ),
    ]

    assert runner(source, environment=environment).nodes == expected


def test_macro_control_if_not_equal():
    environment = Environment.from_dict({"flag": "42"})

    source = '[@if](flag, "!=42", "TRUE", "FALSE")'

    expected = [
        Node(
            children={
                "content": [
                    Node(
                        content=TextNodeContent("FALSE"),
                        info=NodeInfo(context=generate_context(0, 29)),
                    )
                ]
            },
            content=SentenceNodeContent(),
            info=NodeInfo(context=generate_context(0, 0)),
        ),
    ]

    assert runner(source, environment=environment).nodes == expected


def test_macro_control_wrong_name_format():
    environment = Environment.from_dict({"flag": "42"})

    source = '[@if](flag, "TRUE", "FALSE")'

    with pytest.raises(MauParserException):
        runner(source, environment=environment)


def test_macro_control_unsupported_operator():
    environment = Environment.from_dict({"flag": "42"})

    source = '[@something](flag, &true, "TRUE", "FALSE")'

    with pytest.raises(MauParserException):
        runner(source, environment=environment)


def test_macro_control_undefined_variable():
    source = '[@if](flag, &true, "TRUE", "FALSE")'

    with pytest.raises(MauParserException):
        runner(source)


def test_macro_control_invalid_boolean():
    environment = Environment.from_dict({"flag": "42"})

    source = '[@if](flag, &something, "TRUE", "FALSE")'

    with pytest.raises(MauParserException):
        runner(source, environment)


def test_macro_control_invalid_test():
    environment = Environment.from_dict({"flag": "42"})

    source = '[@if](flag, -something, "TRUE", "FALSE")'

    with pytest.raises(MauParserException):
        runner(source, environment)


def test_macro_control_ifeval_true():
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
            children={
                "content": [
                    Node(
                        children={
                            "content": [
                                Node(
                                    content=TextNodeContent("sometext"),
                                    info=NodeInfo(context=generate_context(0, 24)),
                                ),
                            ]
                        },
                        content=StyleNodeContent("underscore"),
                        info=NodeInfo(context=generate_context(0, 23)),
                    )
                ]
            },
            content=SentenceNodeContent(),
            info=NodeInfo(context=generate_context(0, 0)),
        ),
    ]

    assert runner(source, environment=environment).nodes == expected


def test_macro_control_ifeval_false():
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
            children={
                "content": [
                    Node(
                        children={
                            "content": [
                                Node(
                                    content=TextNodeContent("othertext"),
                                    info=NodeInfo(context=generate_context(0, 37)),
                                ),
                            ]
                        },
                        content=StyleNodeContent("star"),
                        info=NodeInfo(context=generate_context(0, 36)),
                    )
                ]
            },
            content=SentenceNodeContent(),
            info=NodeInfo(context=generate_context(0, 0)),
        ),
    ]

    assert runner(source, environment=environment).nodes == expected


def test_macro_control_ifeval_false_is_not_evaluated():
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
            children={
                "content": [
                    Node(
                        children={
                            "content": [
                                Node(
                                    content=TextNodeContent("sometext"),
                                    info=NodeInfo(context=generate_context(0, 24)),
                                ),
                            ]
                        },
                        content=StyleNodeContent("underscore"),
                        info=NodeInfo(context=generate_context(0, 23)),
                    )
                ]
            },
            content=SentenceNodeContent(),
            info=NodeInfo(context=generate_context(0, 0)),
        ),
    ]

    assert runner(source, environment=environment).nodes == expected


def test_macro_control_ifeval_true_is_not_evaluated():
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
            children={
                "content": [
                    Node(
                        children={
                            "content": [
                                Node(
                                    content=TextNodeContent("sometext"),
                                    info=NodeInfo(context=generate_context(0, 33)),
                                ),
                            ]
                        },
                        content=StyleNodeContent("underscore"),
                        info=NodeInfo(context=generate_context(0, 32)),
                    )
                ]
            },
            content=SentenceNodeContent(),
            info=NodeInfo(context=generate_context(0, 0)),
        ),
    ]

    assert runner(source, environment=environment).nodes == expected


def test_macro_control_ifeval_undefined_variable():
    environment = Environment.from_dict({"flag": False})

    source = "[@ifeval](flag, &true, var)"

    with pytest.raises(MauParserException):
        runner(source, environment)


def test_macro_control_ifeval_true_not_defined():
    environment = Environment.from_dict(
        {
            "flag": True,
            "star": "*othertext*",
        }
    )

    source = "[@ifeval](flag, &true, underscore, star)"

    with pytest.raises(MauParserException):
        runner(source, environment)


def test_macro_control_ifeval_false_not_defined():
    environment = Environment.from_dict(
        {
            "flag": True,
            "underscore": "_sometext_",
        }
    )

    source = "[@ifeval](flag, &false, underscore, star)"

    with pytest.raises(MauParserException):
        runner(source, environment)


def test_macro_control_default_false():
    environment = Environment.from_dict({"flag": False})

    source = '[@if](flag, &false, "TRUE")'

    expected = [
        Node(
            children={"content": []},
            content=SentenceNodeContent(),
            info=NodeInfo(context=generate_context(0, 0)),
        ),
    ]

    nodes = runner(source, environment=environment).nodes

    assert nodes == expected


def test_macro_control_without_true_case():
    source = "[@if](flag, &false)"

    with pytest.raises(MauParserException) as exc:
        runner(source)

    assert exc.value.context == generate_context(0, 0)


def test_macro_control_without_value():
    source = "[@if](flag)"

    with pytest.raises(MauParserException) as exc:
        runner(source)

    assert exc.value.context == generate_context(0, 0)


def test_macro_control_without_variable():
    source = "[@if]()"

    with pytest.raises(MauParserException) as exc:
        runner(source)

    assert exc.value.context == generate_context(0, 0)
