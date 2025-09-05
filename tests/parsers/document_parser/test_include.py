from mau.lexers.document_lexer import DocumentLexer
from mau.parsers.document_parser import DocumentParser
from mau.nodes.node import Node, NodeInfo
from mau.nodes.inline import TextNodeContent, SentenceNodeContent
from mau.nodes.include import IncludeNodeContent
from mau.nodes.macros import MacroLinkNodeContent
from mau.nodes.paragraph import ParagraphNodeContent
from mau.test_helpers import (
    init_parser_factory,
    parser_runner_factory,
    generate_context,
    compare_nodes,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_include_content():
    source = """
    << ctype1:/path/to/it,/another/path
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=IncludeNodeContent("ctype1", ["/path/to/it", "/another/path"]),
                info=NodeInfo(context=generate_context(1, 0)),
            ),
        ],
    )


def test_include_content_attributes():
    source = """
    ["text", #tag1, *subtype1, key1=value1]
    << ctype1:/path/to/it,/another/path
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=IncludeNodeContent("ctype1", ["/path/to/it", "/another/path"]),
                info=NodeInfo(
                    context=generate_context(2, 0),
                    subtype="subtype1",
                    unnamed_args=["text"],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                ),
            ),
        ],
    )


# TODO title

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
