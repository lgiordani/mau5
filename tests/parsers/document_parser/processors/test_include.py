import pytest

from mau.environment.environment import Environment
from mau.lexers.document_lexer.lexer import DocumentLexer
from mau.nodes.include import IncludeNodeContent
from mau.nodes.inline import SentenceNodeContent, TextNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.arguments_parser.parser import Arguments
from mau.parsers.base_parser.parser import MauParserException
from mau.parsers.document_parser.parser import DocumentParser
from mau.parsers.document_parser.processors.include import include_processor
from mau.test_helpers import (
    compare_nodes,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_include_content_inline_arguments():
    source = "<< ctype1:/path/to/it, /another/path, #tag1, *subtype1, key1=value1"

    parser: DocumentParser = init_parser(source)
    include_processor(parser)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=IncludeNodeContent("ctype1", ["/path/to/it", "/another/path"]),
                info=NodeInfo(
                    context=generate_context(0, 0),
                    unnamed_args=[],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
            ),
        ],
    )


def test_include_content_boxed_arguments():
    source = "<< ctype1"

    parser: DocumentParser = init_parser(source)
    parser.arguments_manager.push(
        Arguments(
            unnamed_args=["/path/to/it", "/another/path"],
            named_args={"key1": "value1"},
            tags=["tag1"],
            subtype="subtype1",
        )
    )

    include_processor(parser)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=IncludeNodeContent("ctype1", ["/path/to/it", "/another/path"]),
                info=NodeInfo(
                    context=generate_context(0, 0),
                    unnamed_args=[],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
            ),
        ],
    )


def test_include_content_boxed_and_inline_arguments_are_forbidden():
    source = "<< ctype1:/another/path"

    parser: DocumentParser = init_parser(source)
    parser.arguments_manager.push(
        Arguments(
            unnamed_args=["/path/to/it"],
        )
    )

    with pytest.raises(MauParserException) as exc:
        include_processor(parser)

    assert (
        exc.value.message
        == "Syntax error. You cannot specify both boxed and inline arguments."
    )
    assert exc.value.context == generate_context(0, 0)


def test_include_content_without_arguments_is_forbidden():
    source = "<< ctype1"

    with pytest.raises(MauParserException) as exc:
        runner(source)

    assert exc.value.message == "Syntax error. You need to specify a list of URIs."
    assert exc.value.context == generate_context(0, 0)


def test_include_content_without_unnamed_arguments_is_forbidden():
    source = "<< ctype1:key1=value1"

    parser: DocumentParser = init_parser(source)

    with pytest.raises(MauParserException) as exc:
        include_processor(parser)

    assert exc.value.message == "Syntax error. You need to specify a list of URIs."
    assert exc.value.context == generate_context(0, 0)


def test_include_content_with_title():
    source = "<< ctype1:/path/to/it,/another/path"

    parser: DocumentParser = init_parser(source)
    parser.title_manager.push("A title", generate_context(1, 2), Environment())

    include_processor(parser)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=IncludeNodeContent("ctype1", ["/path/to/it", "/another/path"]),
                info=NodeInfo(context=generate_context(0, 0)),
                children={
                    "title": [
                        Node(
                            content=SentenceNodeContent(),
                            info=NodeInfo(context=generate_context(1, 2)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent("A title"),
                                        info=NodeInfo(context=generate_context(1, 2)),
                                    )
                                ]
                            },
                        )
                    ]
                },
            ),
        ],
    )


def test_include_full_parse():
    source = """
    << ctype1:/path/to/it, /another/path, #tag1, *subtype1, key1=value1
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=IncludeNodeContent("ctype1", ["/path/to/it", "/another/path"]),
                info=NodeInfo(
                    context=generate_context(1, 0),
                    unnamed_args=[],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
            ),
        ],
    )


# def test_include_image_with_only_path():
#     source = """
#     << image:/path/to/it.jpg
#     """

#     assert runner(source).nodes == [ContentImageNode("/path/to/it.jpg")]


# def test_include_image_with_http():
#     source = """
#     << image:https:///some.domain/path/to/it.jpg
#     """

#     assert runner(source).nodes == [
#         ContentImageNode("https:///some.domain/path/to/it.jpg")
#     ]


# def test_include_image_with_arguments():
#     source = """
#     ["alt text", #tag1, key1=value1, key2=value2, classes="class1,class2"]
#     << image:/path/to/it.jpg,
#     """

#     assert runner(source).nodes == [
#         ContentImageNode(
#             "/path/to/it.jpg",
#             args=[],
#             tags=["tag1"],
#             kwargs={"key1": "value1", "key2": "value2"},
#             alt_text="alt text",
#             classes=["class1", "class2"],
#         )
#     ]


# def test_include_image_with_title():
#     source = """
#     . A nice caption
#     << image:/path/to/it.jpg
#     """

#     assert runner(source).nodes == [
#         ContentImageNode(
#             "/path/to/it.jpg",
#             title=SentenceNode(
#                 children=[
#                     TextNode("A nice caption"),
#                 ]
#             ),
#         )
#     ]


# def test_include_image_with_subtype():
#     source = """
#     [*subtype1]
#     << image:/path/to/it.jpg
#     """

#     assert runner(source).nodes == [
#         ContentImageNode(
#             "/path/to/it.jpg",
#             subtype="subtype1",
#         ),
#     ]
