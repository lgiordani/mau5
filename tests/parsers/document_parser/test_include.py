import pytest

from mau.environment.environment import Environment
from mau.lexers.document_lexer import DocumentLexer
from mau.nodes.include import IncludeImageNode, IncludeNode
from mau.nodes.inline import TextNode
from mau.nodes.node import NodeInfo
from mau.parsers.base_parser import MauParserException
from mau.parsers.document_parser import DocumentParser
from mau.test_helpers import (
    check_parent,
    compare_nodes_sequence,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_include_content_inline_arguments():
    source = """
    << ctype1:/path/to/it, /another/path, #tag1, *subtype1, key1=value1
    """

    parser = runner(source)

    compare_nodes_sequence(
        parser.nodes,
        [
            IncludeNode(
                "ctype1",
                ["/path/to/it", "/another/path"],
                info=NodeInfo(
                    context=generate_context(1, 0, 1, 9),
                    unnamed_args=[],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
            ),
        ],
    )


def test_include_content_boxed_arguments():
    source = """
    [/path/to/it, /another/path, #tag1, *subtype1, key1=value1]
    << ctype1
    """

    parser = runner(source)

    compare_nodes_sequence(
        parser.nodes,
        [
            IncludeNode(
                "ctype1",
                ["/path/to/it", "/another/path"],
                info=NodeInfo(
                    context=generate_context(2, 0, 2, 9),
                    unnamed_args=[],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
            ),
        ],
    )


def test_include_content_boxed_and_inline_arguments_are_forbidden():
    source = """
    [/path/to/it]
    << ctype1:/another/path
    """

    with pytest.raises(MauParserException) as exc:
        runner(source)

    assert (
        exc.value.message
        == "Syntax error. You cannot specify both boxed and inline arguments."
    )
    assert exc.value.context == generate_context(2, 0, 2, 9)


def test_include_content_without_arguments_is_forbidden():
    source = """
    << ctype1
    """

    with pytest.raises(MauParserException) as exc:
        runner(source)

    assert exc.value.message == "Syntax error. You need to specify a list of URIs."
    assert exc.value.context == generate_context(1, 0, 1, 9)


def test_include_content_without_unnamed_arguments_is_forbidden():
    source = """
    << ctype1:key1=value1
    """

    with pytest.raises(MauParserException) as exc:
        runner(source)

    assert exc.value.message == "Syntax error. You need to specify a list of URIs."
    assert exc.value.context == generate_context(1, 0, 1, 9)


def test_include_content_with_label():
    source = """
    . A title
    << ctype1:/path/to/it,/another/path
    """

    parser = runner(source)

    compare_nodes_sequence(
        parser.nodes,
        [
            IncludeNode(
                "ctype1",
                ["/path/to/it", "/another/path"],
                labels={
                    "title": [
                        TextNode(
                            "A title",
                            info=NodeInfo(context=generate_context(1, 2, 1, 9)),
                        )
                    ]
                },
                info=NodeInfo(context=generate_context(2, 0, 2, 9)),
            )
        ],
    )


def test_header_uses_control_positive():
    environment = Environment()
    environment["answer"] = "42"

    source = """
    @if answer==42
    << ctype1:/path/to/it
    """

    parser = runner(source, environment)

    compare_nodes_sequence(
        parser.nodes,
        [
            IncludeNode(
                "ctype1",
                ["/path/to/it"],
                info=NodeInfo(
                    context=generate_context(2, 0, 2, 9),
                    unnamed_args=[],
                    named_args={},
                    tags=[],
                    subtype=None,
                ),
            ),
        ],
    )

    assert parser.control_buffer.pop() is None


def test_header_uses_control_negative():
    environment = Environment()
    environment["answer"] = "24"

    source = """
    @if answer==42
    << ctype1:/path/to/it
    """

    parser = runner(source, environment)

    compare_nodes_sequence(parser.nodes, [])


def test_include_image_with_only_path():
    source = """
    << image:/path/to/it.jpg
    """

    parser = runner(source)

    compare_nodes_sequence(
        parser.nodes,
        [
            IncludeImageNode(
                "/path/to/it.jpg",
                info=NodeInfo(
                    context=generate_context(1, 0, 1, 8),
                    unnamed_args=[],
                    named_args={},
                    tags=[],
                    subtype=None,
                ),
            ),
        ],
    )


def test_include_image_with_alt_text_and_classes():
    source = """
    << image:/path/to/it.jpg, "Alt text", "class1,class2"
    """

    parser = runner(source)

    compare_nodes_sequence(
        parser.nodes,
        [
            IncludeImageNode(
                "/path/to/it.jpg",
                "Alt text",
                ["class1", "class2"],
                info=NodeInfo(
                    context=generate_context(1, 0, 1, 8),
                    unnamed_args=[],
                    named_args={},
                    tags=[],
                    subtype=None,
                ),
            ),
        ],
    )


def test_include_image_without_uri():
    source = """
    << image"
    """

    with pytest.raises(MauParserException) as exc:
        runner(source)

    assert exc.value.context == generate_context(1, 0, 1, 8)


def test_include_parenthood():
    source = """
    << ctype1:/path/to/it
    """

    parser = runner(source)

    document_node = parser.output.document

    # All parser nodes must be
    # children of the document node.
    check_parent(document_node, parser.nodes)


def test_list_parenthood_labels():
    source = """
    . A label
    .role Another label
    << ctype1:/path/to/it
    """

    parser = runner(source)

    include_node = parser.nodes[0]
    label_title_nodes = include_node.labels["title"]
    label_role_nodes = include_node.labels["role"]

    # Each label must be a child of the
    # include node it has been assigned to.
    check_parent(include_node, label_title_nodes)
    check_parent(include_node, label_role_nodes)
