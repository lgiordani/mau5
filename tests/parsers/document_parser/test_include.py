from unittest.mock import call, mock_open, patch

import pytest

from mau.environment.environment import Environment
from mau.lexers.document_lexer import DocumentLexer
from mau.message import MauException, MauMessageType
from mau.nodes.include import IncludeImageNode, IncludeMauNode, IncludeNode
from mau.nodes.inline import TextNode
from mau.nodes.node import NodeInfo
from mau.nodes.node_arguments import NodeArguments
from mau.nodes.paragraph import ParagraphLineNode, ParagraphNode
from mau.parsers.document_parser import DocumentParser
from mau.parsers.document_processors.include import IncludeCall
from mau.test_helpers import (
    TEST_CONTEXT_SOURCE,
    check_parent,
    compare_nodes_sequence,
    dedent,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)
from mau.text_buffer import Context

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
                arguments=NodeArguments(
                    unnamed_args=["/path/to/it", "/another/path"],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
                info=NodeInfo(
                    context=generate_context(1, 0, 1, 9),
                ),
            ),
        ],
    )


def test_include_content_without_arguments():
    source = """
    << ctype1
    """

    parser = runner(source)

    compare_nodes_sequence(
        parser.nodes,
        [
            IncludeNode(
                "ctype1",
                arguments=NodeArguments(
                    unnamed_args=[],
                    named_args={},
                    tags=[],
                    subtype=None,
                ),
                info=NodeInfo(
                    context=generate_context(1, 0, 1, 9),
                ),
            ),
        ],
    )


def test_include_inline_arguments_support_variables():
    environment = Environment.from_dict(
        {
            "paths": "/path/to/it, /another/path",
            "keyvalue": "key1=value1",
            "tag_with_prefix": "#tag1",
            "subtype_with_prefix": "*subtype1",
        }
    )

    source = """
    << ctype1:{paths}, {tag_with_prefix}, {subtype_with_prefix}, {keyvalue}
    """

    parser = runner(source, environment)

    compare_nodes_sequence(
        parser.nodes,
        [
            IncludeNode(
                "ctype1",
                arguments=NodeArguments(
                    unnamed_args=["/path/to/it", "/another/path"],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
                info=NodeInfo(
                    context=generate_context(1, 0, 1, 9),
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
                arguments=NodeArguments(
                    unnamed_args=["/path/to/it", "/another/path"],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
                info=NodeInfo(
                    context=generate_context(2, 0, 2, 9),
                ),
            ),
        ],
    )


def test_include_content_boxed_and_inline_arguments_are_forbidden():
    source = """
    [/path/to/it]
    << ctype1:/another/path
    """

    with pytest.raises(MauException) as exc:
        runner(source)

    assert exc.value.message.type == MauMessageType.ERROR_PARSER
    assert (
        exc.value.message.text
        == "Syntax error. You cannot specify both boxed and inline arguments."
    )
    assert exc.value.message.context == generate_context(2, 0, 2, 9)


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
                arguments=NodeArguments(
                    unnamed_args=["/path/to/it", "/another/path"],
                    named_args={},
                    tags=[],
                    subtype=None,
                ),
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
                arguments=NodeArguments(
                    unnamed_args=["/path/to/it"],
                    named_args={},
                    tags=[],
                    subtype=None,
                ),
                info=NodeInfo(
                    context=generate_context(2, 0, 2, 9),
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
                arguments=NodeArguments(
                    unnamed_args=[],
                    named_args={},
                    tags=[],
                    subtype=None,
                ),
                info=NodeInfo(
                    context=generate_context(1, 0, 1, 8),
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
                arguments=NodeArguments(
                    unnamed_args=[],
                    named_args={},
                    tags=[],
                    subtype=None,
                ),
                info=NodeInfo(
                    context=generate_context(1, 0, 1, 8),
                ),
            ),
        ],
    )


def test_include_image_without_uri():
    source = """
    << image"
    """

    with pytest.raises(MauException) as exc:
        runner(source)

    assert exc.value.message.type == MauMessageType.ERROR_PARSER
    assert exc.value.message.text == "Syntax error. You need to specify a URI."
    assert exc.value.message.context == generate_context(1, 0, 1, 8)


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


def test_include_mau():
    # This tests that Mau can include
    # a file that contains Mau code
    # and add the parsed tree of that
    # file to the current one.

    source = """
    << mau:/path/to/it
    """

    MAU_TEXT = dedent("""
    This is a paragraph.
    This is part of the same paragraph.

    This is another paragraph.
    """)

    with patch("builtins.open", mock_open(read_data=MAU_TEXT)) as mock_file:
        parser = runner(source)

    compare_nodes_sequence(
        parser.nodes,
        [
            IncludeMauNode(
                "/path/to/it",
                arguments=NodeArguments(
                    unnamed_args=[],
                    named_args={},
                    tags=[],
                    subtype=None,
                ),
                info=NodeInfo(
                    context=generate_context(1, 0, 1, 6),
                ),
                content=[
                    ParagraphNode(
                        lines=[
                            ParagraphLineNode(
                                content=[
                                    TextNode(
                                        "This is a paragraph.",
                                        info=NodeInfo(
                                            context=Context(1, 0, 1, 20, "/path/to/it")
                                        ),
                                    ),
                                ],
                                info=NodeInfo(
                                    context=Context(1, 0, 1, 20, "/path/to/it")
                                ),
                            ),
                            ParagraphLineNode(
                                content=[
                                    TextNode(
                                        "This is part of the same paragraph.",
                                        info=NodeInfo(
                                            context=Context(2, 0, 2, 35, "/path/to/it")
                                        ),
                                    ),
                                ],
                                info=NodeInfo(
                                    context=Context(2, 0, 2, 35, "/path/to/it")
                                ),
                            ),
                        ],
                        info=NodeInfo(context=Context(1, 0, 2, 35, "/path/to/it")),
                    ),
                    ParagraphNode(
                        lines=[
                            ParagraphLineNode(
                                content=[
                                    TextNode(
                                        "This is another paragraph.",
                                        info=NodeInfo(
                                            context=Context(4, 0, 4, 26, "/path/to/it")
                                        ),
                                    ),
                                ],
                                info=NodeInfo(
                                    context=Context(4, 0, 4, 26, "/path/to/it")
                                ),
                            )
                        ],
                        info=NodeInfo(context=Context(4, 0, 4, 26, "/path/to/it")),
                    ),
                ],
            ),
        ],
    )

    mock_file.assert_called_with("/path/to/it", "r", encoding="utf-8")

    assert parser.output.include_calls == [
        IncludeCall(
            caller_uri=TEST_CONTEXT_SOURCE,
            callee_uri="/path/to/it",
            call_arguments={},
            info=NodeInfo(context=generate_context(1, 0, 1, 6)),
        )
    ]


def test_include_mau_without_uri():
    source = """
    << mau"
    """

    with pytest.raises(MauException) as exc:
        runner(source)

    assert exc.value.message.type == MauMessageType.ERROR_PARSER
    assert exc.value.message.text == "Syntax error. You need to specify a URI."
    assert exc.value.message.context == generate_context(1, 0, 1, 6)


def test_include_mau_recursively():
    # This tests that Mau inclusion can
    # be done recursively, with the
    # included file containing
    # syntax to include another file.

    source = """
    << mau:/path/to/it
    """

    MAU_TEXT_1 = dedent("""
    << mau:/another/path
    """)

    MAU_TEXT_2 = dedent("""
    This is a paragraph.
    """)

    m1 = mock_open(read_data=MAU_TEXT_1)
    m2 = mock_open(read_data=MAU_TEXT_2)

    with patch(
        "builtins.open", side_effect=[m1.return_value, m2.return_value]
    ) as mock_file:
        parser = runner(source)

    compare_nodes_sequence(
        parser.nodes,
        [
            IncludeMauNode(
                "/path/to/it",
                arguments=NodeArguments(
                    unnamed_args=[],
                    named_args={},
                    tags=[],
                    subtype=None,
                ),
                info=NodeInfo(
                    context=generate_context(1, 0, 1, 6),
                ),
                content=[
                    IncludeMauNode(
                        "/another/path",
                        arguments=NodeArguments(
                            unnamed_args=[],
                            named_args={},
                            tags=[],
                            subtype=None,
                        ),
                        info=NodeInfo(
                            context=Context(1, 0, 1, 6, source="/path/to/it"),
                        ),
                        content=[
                            ParagraphNode(
                                lines=[
                                    ParagraphLineNode(
                                        content=[
                                            TextNode(
                                                "This is a paragraph.",
                                                info=NodeInfo(
                                                    context=Context(
                                                        1, 0, 1, 20, "/another/path"
                                                    )
                                                ),
                                            ),
                                        ],
                                        info=NodeInfo(
                                            context=Context(
                                                1, 0, 1, 20, "/another/path"
                                            )
                                        ),
                                    ),
                                ],
                                info=NodeInfo(
                                    context=Context(1, 0, 1, 20, "/another/path")
                                ),
                            )
                        ],
                    )
                ],
            )
        ],
    )

    mock_file.assert_has_calls(
        [
            call("/path/to/it", "r", encoding="utf-8"),
            call("/another/path", "r", encoding="utf-8"),
        ]
    )

    assert parser.output.include_calls == [
        IncludeCall(
            caller_uri=TEST_CONTEXT_SOURCE,
            callee_uri="/path/to/it",
            call_arguments={},
            info=NodeInfo(context=generate_context(1, 0, 1, 6)),
        ),
        IncludeCall(
            caller_uri="/path/to/it",
            callee_uri="/another/path",
            call_arguments={},
            info=NodeInfo(context=Context(1, 0, 1, 6, source="/path/to/it")),
        ),
    ]


def test_include_mau_environment():
    # This tests that included files
    # have access to the full
    # environment of the includer.

    source = """
    :answer:42
    
    << mau:/path/to/it
    """

    MAU_TEXT = dedent("""
    The answer is {answer}.
    """)

    with patch("builtins.open", mock_open(read_data=MAU_TEXT)) as mock_file:
        parser = runner(source)

    compare_nodes_sequence(
        parser.nodes,
        [
            IncludeMauNode(
                "/path/to/it",
                arguments=NodeArguments(
                    unnamed_args=[],
                    named_args={},
                    tags=[],
                    subtype=None,
                ),
                info=NodeInfo(
                    context=generate_context(3, 0, 3, 6),
                ),
                content=[
                    ParagraphNode(
                        lines=[
                            ParagraphLineNode(
                                content=[
                                    TextNode(
                                        "The answer is 42.",
                                        info=NodeInfo(
                                            context=Context(3, 0, 3, 17, "/path/to/it")
                                        ),
                                    ),
                                ],
                                info=NodeInfo(
                                    context=Context(3, 0, 3, 23, "/path/to/it")
                                ),
                            ),
                        ],
                        info=NodeInfo(context=Context(3, 0, 3, 23, "/path/to/it")),
                    )
                ],
            ),
        ],
    )

    mock_file.assert_called_with("/path/to/it", "r", encoding="utf-8")

    assert parser.output.include_calls == [
        IncludeCall(
            caller_uri=TEST_CONTEXT_SOURCE,
            callee_uri="/path/to/it",
            call_arguments={},
            info=NodeInfo(context=generate_context(3, 0, 3, 6)),
        )
    ]


def test_include_mau_custom_arguments():
    # This tests that included files
    # can be given custom arguments
    # that are added to their environment.

    source = """
    :answer:42
    
    << mau:/path/to/it, call:target="Life, the Universe, and Everything"
    """

    MAU_TEXT = dedent("""
    The answer to {target} is {answer}.
    """)

    with patch("builtins.open", mock_open(read_data=MAU_TEXT)) as mock_file:
        parser = runner(source)

    compare_nodes_sequence(
        parser.nodes,
        [
            IncludeMauNode(
                "/path/to/it",
                arguments=NodeArguments(
                    unnamed_args=[],
                    named_args={},
                    tags=[],
                    subtype=None,
                ),
                info=NodeInfo(
                    context=generate_context(3, 0, 3, 6),
                ),
                content=[
                    ParagraphNode(
                        lines=[
                            ParagraphLineNode(
                                content=[
                                    TextNode(
                                        "The answer to Life, the Universe, and Everything is 42.",
                                        info=NodeInfo(
                                            context=Context(3, 0, 3, 55, "/path/to/it")
                                        ),
                                    ),
                                ],
                                info=NodeInfo(
                                    context=Context(3, 0, 3, 35, "/path/to/it")
                                ),
                            ),
                        ],
                        info=NodeInfo(context=Context(3, 0, 3, 35, "/path/to/it")),
                    )
                ],
            ),
        ],
    )

    mock_file.assert_called_with("/path/to/it", "r", encoding="utf-8")

    assert parser.output.include_calls == [
        IncludeCall(
            caller_uri=TEST_CONTEXT_SOURCE,
            callee_uri="/path/to/it",
            call_arguments={"target": "Life, the Universe, and Everything"},
            info=NodeInfo(context=generate_context(3, 0, 3, 6)),
        )
    ]


def test_include_mau_custom_arguments_passed_recursively_automatic():
    # This tests that included files automatically
    # pass the arguments they have been given to
    # other files that they include.
    # This is just a double-check, as it is
    # granted by the fact that the inclusion
    # passes the includer environment.

    source = """
    :answer:42
    
    << mau:/path/to/it, call:target="Life, the Universe, and Everything"
    """

    MAU_TEXT_1 = dedent("""
    << mau:/another/path, call:target="{target}"
    """)

    MAU_TEXT_2 = dedent("""
    The answer to {target} is {answer}.
    """)

    m1 = mock_open(read_data=MAU_TEXT_1)
    m2 = mock_open(read_data=MAU_TEXT_2)

    with patch(
        "builtins.open", side_effect=[m1.return_value, m2.return_value]
    ) as mock_file:
        parser = runner(source)

    compare_nodes_sequence(
        parser.nodes,
        [
            IncludeMauNode(
                "/path/to/it",
                arguments=NodeArguments(
                    unnamed_args=[],
                    named_args={},
                    tags=[],
                    subtype=None,
                ),
                info=NodeInfo(
                    context=generate_context(3, 0, 3, 6),
                ),
                content=[
                    IncludeMauNode(
                        "/another/path",
                        arguments=NodeArguments(
                            unnamed_args=[],
                            named_args={},
                            tags=[],
                            subtype=None,
                        ),
                        info=NodeInfo(
                            context=Context(3, 0, 3, 6, source="/path/to/it"),
                        ),
                        content=[
                            ParagraphNode(
                                lines=[
                                    ParagraphLineNode(
                                        content=[
                                            TextNode(
                                                "The answer to Life, the Universe, and Everything is 42.",
                                                info=NodeInfo(
                                                    context=Context(
                                                        3, 0, 3, 55, "/another/path"
                                                    )
                                                ),
                                            ),
                                        ],
                                        info=NodeInfo(
                                            context=Context(
                                                3, 0, 3, 35, "/another/path"
                                            )
                                        ),
                                    ),
                                ],
                                info=NodeInfo(
                                    context=Context(3, 0, 3, 35, "/another/path")
                                ),
                            )
                        ],
                    )
                ],
            )
        ],
    )

    mock_file.assert_has_calls(
        [
            call("/path/to/it", "r", encoding="utf-8"),
            call("/another/path", "r", encoding="utf-8"),
        ]
    )

    assert parser.output.include_calls == [
        IncludeCall(
            caller_uri=TEST_CONTEXT_SOURCE,
            callee_uri="/path/to/it",
            call_arguments={"target": "Life, the Universe, and Everything"},
            info=NodeInfo(context=generate_context(3, 0, 3, 6)),
        ),
        IncludeCall(
            caller_uri="/path/to/it",
            callee_uri="/another/path",
            call_arguments={"target": "Life, the Universe, and Everything"},
            info=NodeInfo(context=Context(3, 0, 3, 6, source="/path/to/it")),
        ),
    ]


def test_include_mau_custom_arguments_passed_recursively_explicitly():
    # This tests that included files can explicitly
    # pass the arguments they have been given to
    # other files that they include.

    source = """
    :answer:42
    
    << mau:/path/to/it, call:target="Life, the Universe, and Everything"
    """

    MAU_TEXT_1 = dedent("""
    << mau:/another/path, call:target="{target}"
    """)

    MAU_TEXT_2 = dedent("""
    The answer to {target} is {answer}.
    """)

    m1 = mock_open(read_data=MAU_TEXT_1)
    m2 = mock_open(read_data=MAU_TEXT_2)

    with patch(
        "builtins.open", side_effect=[m1.return_value, m2.return_value]
    ) as mock_file:
        parser = runner(source)

    compare_nodes_sequence(
        parser.nodes,
        [
            IncludeMauNode(
                "/path/to/it",
                arguments=NodeArguments(
                    unnamed_args=[],
                    named_args={},
                    tags=[],
                    subtype=None,
                ),
                info=NodeInfo(
                    context=generate_context(3, 0, 3, 6),
                ),
                content=[
                    IncludeMauNode(
                        "/another/path",
                        arguments=NodeArguments(
                            unnamed_args=[],
                            named_args={},
                            tags=[],
                            subtype=None,
                        ),
                        info=NodeInfo(
                            context=Context(3, 0, 3, 6, source="/path/to/it"),
                        ),
                        content=[
                            ParagraphNode(
                                lines=[
                                    ParagraphLineNode(
                                        content=[
                                            TextNode(
                                                "The answer to Life, the Universe, and Everything is 42.",
                                                info=NodeInfo(
                                                    context=Context(
                                                        3, 0, 3, 55, "/another/path"
                                                    )
                                                ),
                                            ),
                                        ],
                                        info=NodeInfo(
                                            context=Context(
                                                3, 0, 3, 35, "/another/path"
                                            )
                                        ),
                                    ),
                                ],
                                info=NodeInfo(
                                    context=Context(3, 0, 3, 35, "/another/path")
                                ),
                            )
                        ],
                    )
                ],
            )
        ],
    )

    mock_file.assert_has_calls(
        [
            call("/path/to/it", "r", encoding="utf-8"),
            call("/another/path", "r", encoding="utf-8"),
        ]
    )

    assert parser.output.include_calls == [
        IncludeCall(
            caller_uri=TEST_CONTEXT_SOURCE,
            callee_uri="/path/to/it",
            call_arguments={"target": "Life, the Universe, and Everything"},
            info=NodeInfo(context=generate_context(3, 0, 3, 6)),
        ),
        IncludeCall(
            caller_uri="/path/to/it",
            callee_uri="/another/path",
            call_arguments={"target": "Life, the Universe, and Everything"},
            info=NodeInfo(context=Context(3, 0, 3, 6, source="/path/to/it")),
        ),
    ]


def test_include_mau_custom_arguments_passed_recursively_overwrite():
    # This tests that included files can overwrite
    # the arguments they have been given when passing
    # arguments to other files that they include.

    source = """
    :answer:42
    
    << mau:/path/to/it, call:target="Life, the Universe, and Everything"
    """

    MAU_TEXT_1 = dedent("""
    << mau:/another/path, call:target="the Question"
    """)

    MAU_TEXT_2 = dedent("""
    The answer to {target} is {answer}.
    """)

    m1 = mock_open(read_data=MAU_TEXT_1)
    m2 = mock_open(read_data=MAU_TEXT_2)

    with patch(
        "builtins.open", side_effect=[m1.return_value, m2.return_value]
    ) as mock_file:
        parser = runner(source)

    compare_nodes_sequence(
        parser.nodes,
        [
            IncludeMauNode(
                "/path/to/it",
                arguments=NodeArguments(
                    unnamed_args=[],
                    named_args={},
                    tags=[],
                    subtype=None,
                ),
                info=NodeInfo(
                    context=generate_context(3, 0, 3, 6),
                ),
                content=[
                    IncludeMauNode(
                        "/another/path",
                        arguments=NodeArguments(
                            unnamed_args=[],
                            named_args={},
                            tags=[],
                            subtype=None,
                        ),
                        info=NodeInfo(
                            context=Context(3, 0, 3, 6, source="/path/to/it"),
                        ),
                        content=[
                            ParagraphNode(
                                lines=[
                                    ParagraphLineNode(
                                        content=[
                                            TextNode(
                                                "The answer to the Question is 42.",
                                                info=NodeInfo(
                                                    context=Context(
                                                        3, 0, 3, 33, "/another/path"
                                                    )
                                                ),
                                            ),
                                        ],
                                        info=NodeInfo(
                                            context=Context(
                                                3, 0, 3, 35, "/another/path"
                                            )
                                        ),
                                    ),
                                ],
                                info=NodeInfo(
                                    context=Context(3, 0, 3, 35, "/another/path")
                                ),
                            )
                        ],
                    )
                ],
            )
        ],
    )

    mock_file.assert_has_calls(
        [
            call("/path/to/it", "r", encoding="utf-8"),
            call("/another/path", "r", encoding="utf-8"),
        ]
    )

    assert parser.output.include_calls == [
        IncludeCall(
            caller_uri=TEST_CONTEXT_SOURCE,
            callee_uri="/path/to/it",
            call_arguments={"target": "Life, the Universe, and Everything"},
            info=NodeInfo(context=generate_context(3, 0, 3, 6)),
        ),
        IncludeCall(
            caller_uri="/path/to/it",
            callee_uri="/another/path",
            call_arguments={"target": "the Question"},
            info=NodeInfo(context=Context(3, 0, 3, 6, source="/path/to/it")),
        ),
    ]


def test_include_mau_self_inclusion_is_forbidden():
    # This tests that Mau files cannot
    # include themselves.

    environment = Environment.from_dict({"source": TEST_CONTEXT_SOURCE})

    source = """
    << mau:{source}
    """

    with pytest.raises(MauException) as exc:
        runner(source, environment)

    assert exc.value.message.type == MauMessageType.ERROR_PARSER
    assert (
        exc.value.message.text
        == f"To avoid recursion, you cannot include the following files: ['{TEST_CONTEXT_SOURCE}']."
    )
    assert exc.value.message.context == generate_context(1, 0, 1, 6)


def test_include_mau_loop_is_forbidden():
    # This tests that Mau inclusion detects if
    # a loop occurs, where an included file
    # includes one of the callers.

    source = """
    << mau:/path/to/it
    """

    MAU_TEXT_1 = dedent("""
    << mau:/another/path
    """)

    MAU_TEXT_2 = dedent("""
    << mau:/path/to/it
    """)

    m1 = mock_open(read_data=MAU_TEXT_1)
    m2 = mock_open(read_data=MAU_TEXT_2)

    with pytest.raises(MauException) as exc:
        with patch(
            "builtins.open",
            side_effect=[
                m1.return_value,
                m2.return_value,
            ],
        ):
            runner(source)

    assert exc.value.message.type == MauMessageType.ERROR_PARSER
    assert (
        exc.value.message.text
        == f"To avoid recursion, you cannot include the following files: ['{TEST_CONTEXT_SOURCE}', '/path/to/it', '/another/path']."
    )
    assert exc.value.message.context == Context(1, 0, 1, 6, source="/another/path")
