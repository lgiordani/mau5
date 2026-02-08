import pytest

from mau.environment.environment import Environment
from mau.lexers.document_lexer import DocumentLexer
from mau.message import MauException, MauMessageType
from mau.nodes.command import CommandNode
from mau.nodes.node import NodeInfo
from mau.nodes.node_arguments import NodeArguments
from mau.parsers.document_parser import DocumentParser
from mau.test_helpers import (
    compare_nodes_sequence,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_command_boxed_and_inline_arguments_are_forbidden():
    source = """
    [arg1, #tag1, *subtype1, key1=value1]
    ::cmd:arg2
    """

    with pytest.raises(MauException) as exc:
        runner(source)

    assert exc.value.message.type == MauMessageType.ERROR_PARSER
    assert (
        exc.value.message.text
        == "Syntax error. You cannot specify both boxed and inline arguments."
    )
    assert exc.value.message.context == generate_context(2, 0, 2, 5)


def test_command_colon_after_command_requires_arguments():
    source = """
    ::cmd:
    """

    with pytest.raises(MauException) as exc:
        runner(source)

    assert exc.value.message.type == MauMessageType.ERROR_PARSER
    assert (
        exc.value.message.text
        == "Syntax error. If you use the colon after 'cmd' you need to specify arguments."
    )
    assert exc.value.message.context == generate_context(1, 0, 1, 5)


def test_command_control():
    source = """
    :answer:44

    @if answer==42
    [arg1, arg2]
    . Some title
    ::cmd
    """

    parser = runner(source)

    compare_nodes_sequence(parser.nodes, [])

    assert parser.arguments_buffer.arguments is None
    assert parser.label_buffer.labels == {}
    assert parser.control_buffer.control is None


def test_command_inline_arguments_support_variables():
    environment = Environment.from_dict(
        {
            "args": "arg1, arg2",
            "keyvalue": "key1=value1",
            "tag_with_prefix": "#tag1",
            "subtype_with_prefix": "*subtype1",
        }
    )

    source = """
    ::cmd:{args}, {tag_with_prefix}, {subtype_with_prefix}, {keyvalue}
    """

    parser = runner(source, environment)

    compare_nodes_sequence(
        parser.nodes,
        [
            CommandNode(
                name="cmd",
                arguments=NodeArguments(
                    unnamed_args=["arg1", "arg2"],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
                info=NodeInfo(
                    context=generate_context(1, 0, 1, 5),
                ),
            )
        ],
    )
