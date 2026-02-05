import pytest

from mau.environment.environment import Environment
from mau.error import MauException, MauMessageType
from mau.lexers.text_lexer import TextLexer
from mau.nodes.inline import StyleNode, TextNode
from mau.nodes.node import NodeInfo
from mau.parsers.text_parser import TextParser
from mau.test_helpers import (
    compare_nodes_sequence,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(TextLexer, TextParser)

runner = parser_runner_factory(TextLexer, TextParser)


def test_macro_control_if_true():
    environment = Environment.from_dict({"flag": True})

    source = '[@if](flag, &true, "TRUE", "FALSE")'

    expected = [
        TextNode(
            "TRUE",
            info=NodeInfo(context=generate_context(0, 20, 0, 24)),
        )
    ]

    parser = runner(source, environment=environment)

    compare_nodes_sequence(parser.nodes, expected)


def test_macro_control_if_false():
    environment = Environment.from_dict({"flag": True})

    source = '[@if](flag, &false, "TRUE", "FALSE")'

    expected = [
        TextNode(
            "FALSE",
            info=NodeInfo(context=generate_context(0, 29, 0, 34)),
        )
    ]

    parser = runner(source, environment=environment)

    compare_nodes_sequence(parser.nodes, expected)


def test_macro_control_if_equal():
    environment = Environment.from_dict({"flag": "42"})

    source = '[@if](flag, "=42", "TRUE", "FALSE")'

    expected = [
        TextNode(
            "TRUE",
            info=NodeInfo(context=generate_context(0, 20, 0, 24)),
        )
    ]

    parser = runner(source, environment=environment)

    compare_nodes_sequence(parser.nodes, expected)


def test_macro_control_if_not_equal():
    environment = Environment.from_dict({"flag": "42"})

    source = '[@if](flag, "!=42", "TRUE", "FALSE")'

    expected = [
        TextNode(
            "FALSE",
            info=NodeInfo(context=generate_context(0, 29, 0, 34)),
        )
    ]

    parser = runner(source, environment=environment)

    compare_nodes_sequence(parser.nodes, expected)


def test_macro_control_wrong_name_format():
    environment = Environment.from_dict({"flag": "42"})

    source = '[@if](flag, "TRUE", "FALSE")'

    with pytest.raises(MauException) as exc:
        runner(source, environment=environment)

    assert exc.value.message.type == MauMessageType.ERROR_PARSER


def test_macro_control_unsupported_operator():
    environment = Environment.from_dict({"flag": "42"})

    source = '[@something](flag, &true, "TRUE", "FALSE")'

    with pytest.raises(MauException) as exc:
        runner(source, environment=environment)

    assert exc.value.message.type == MauMessageType.ERROR_PARSER


def test_macro_control_undefined_variable():
    source = '[@if](flag, &true, "TRUE", "FALSE")'

    with pytest.raises(MauException) as exc:
        runner(source)

    assert exc.value.message.type == MauMessageType.ERROR_PARSER


def test_macro_control_invalid_boolean():
    environment = Environment.from_dict({"flag": "42"})

    source = '[@if](flag, &something, "TRUE", "FALSE")'

    with pytest.raises(MauException) as exc:
        runner(source, environment)

    assert exc.value.message.type == MauMessageType.ERROR_PARSER


def test_macro_control_invalid_test():
    environment = Environment.from_dict({"flag": "42"})

    source = '[@if](flag, -something, "TRUE", "FALSE")'

    with pytest.raises(MauException) as exc:
        runner(source, environment)

    assert exc.value.message.type == MauMessageType.ERROR_PARSER


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
        StyleNode(
            "underscore",
            content=[
                TextNode(
                    "sometext",
                    info=NodeInfo(context=generate_context(0, 24, 0, 32)),
                ),
            ],
            info=NodeInfo(context=generate_context(0, 23, 0, 33)),
        )
    ]

    parser = runner(source, environment=environment)

    compare_nodes_sequence(parser.nodes, expected)


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
        StyleNode(
            "star",
            content=[
                TextNode(
                    "othertext",
                    info=NodeInfo(context=generate_context(0, 37, 0, 46)),
                ),
            ],
            info=NodeInfo(context=generate_context(0, 36, 0, 47)),
        )
    ]

    parser = runner(source, environment=environment)

    compare_nodes_sequence(parser.nodes, expected)


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
        StyleNode(
            "underscore",
            content=[
                TextNode(
                    "sometext",
                    info=NodeInfo(context=generate_context(0, 24, 0, 32)),
                ),
            ],
            info=NodeInfo(context=generate_context(0, 23, 0, 33)),
        )
    ]

    parser = runner(source, environment=environment)

    compare_nodes_sequence(parser.nodes, expected)


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
        StyleNode(
            "underscore",
            content=[
                TextNode(
                    "sometext",
                    info=NodeInfo(context=generate_context(0, 33, 0, 41)),
                ),
            ],
            info=NodeInfo(context=generate_context(0, 32, 0, 42)),
        )
    ]

    parser = runner(source, environment=environment)

    compare_nodes_sequence(parser.nodes, expected)


def test_macro_control_ifeval_undefined_variable():
    environment = Environment.from_dict({"flag": False})

    source = "[@ifeval](flag, &true, var)"

    with pytest.raises(MauException) as exc:
        runner(source, environment)

    assert exc.value.message.type == MauMessageType.ERROR_PARSER


def test_macro_control_ifeval_true_not_defined():
    environment = Environment.from_dict(
        {
            "flag": True,
            "star": "*othertext*",
        }
    )

    source = "[@ifeval](flag, &true, underscore, star)"

    with pytest.raises(MauException) as exc:
        runner(source, environment)

    assert exc.value.message.type == MauMessageType.ERROR_PARSER


def test_macro_control_ifeval_false_not_defined():
    environment = Environment.from_dict(
        {
            "flag": True,
            "underscore": "_sometext_",
        }
    )

    source = "[@ifeval](flag, &false, underscore, star)"

    with pytest.raises(MauException) as exc:
        runner(source, environment)

    assert exc.value.message.type == MauMessageType.ERROR_PARSER


def test_macro_control_default_false():
    environment = Environment.from_dict({"flag": False})

    source = '[@if](flag, &false, "TRUE")'

    nodes = runner(source, environment=environment).nodes

    assert nodes == []


def test_macro_control_without_true_case():
    source = "[@if](flag, &false)"

    with pytest.raises(MauException) as exc:
        runner(source)

    assert exc.value.message.type == MauMessageType.ERROR_PARSER
    assert exc.value.message.context == generate_context(0, 0, 0, 19)


def test_macro_control_without_value():
    source = "[@if](flag)"

    with pytest.raises(MauException) as exc:
        runner(source)

    assert exc.value.message.type == MauMessageType.ERROR_PARSER
    assert exc.value.message.context == generate_context(0, 0, 0, 11)


def test_macro_control_without_variable():
    source = "[@if]()"

    with pytest.raises(MauException) as exc:
        runner(source)

    assert exc.value.message.type == MauMessageType.ERROR_PARSER
    assert exc.value.message.context == generate_context(0, 0, 0, 7)
