import pytest

from mau.environment.environment import Environment
from mau.lexers.document_lexer.lexer import DocumentLexer
from mau.nodes.headers import HeaderNodeContent
from mau.nodes.inline import SentenceNodeContent, TextNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.nodes.toc import TocItemNodeContent, TocNodeContent
from mau.parsers.arguments_parser.parser import Arguments
from mau.parsers.base_parser.parser import MauParserException
from mau.parsers.document_parser.parser import DocumentParser
from mau.parsers.document_parser.processors.command import command_processor
from mau.test_helpers import (
    compare_nodes,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_command_toc():
    source = "::toc"

    parser: DocumentParser = init_parser(source)
    command_processor(parser)

    compare_nodes(
        parser.nodes,
        [Node(content=TocNodeContent(), info=NodeInfo(context=generate_context(0, 0)))],
    )


def test_command_toc_inline_arguments():
    source = "::toc:arg1,#tag1,*subtype1,key1=value1"

    parser: DocumentParser = init_parser(source)
    command_processor(parser)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=TocNodeContent(),
                info=NodeInfo(
                    context=generate_context(0, 0),
                    unnamed_args=["arg1"],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
            )
        ],
    )


def test_command_toc_boxed_arguments():
    source = "::toc"

    parser: DocumentParser = init_parser(source)
    parser.arguments_buffer.push(
        Arguments(
            unnamed_args=["arg1"],
            named_args={"key1": "value1"},
            tags=["tag1"],
            subtype="subtype1",
        )
    )

    command_processor(parser)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=TocNodeContent(),
                info=NodeInfo(
                    context=generate_context(0, 0),
                    unnamed_args=["arg1"],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
            )
        ],
    )


def test_command_toc_boxed_and_inline_arguments_are_forbidden():
    source = "::toc:arg2"

    parser: DocumentParser = init_parser(source)
    parser.arguments_buffer.push(
        Arguments(
            unnamed_args=["arg1"],
            named_args={"key1": "value1"},
            tags=["tag1"],
            subtype="subtype1",
        )
    )

    with pytest.raises(MauParserException) as exc:
        command_processor(parser)

    assert (
        exc.value.message
        == "Syntax error. You cannot specify both boxed and inline arguments."
    )
    assert exc.value.context == generate_context(0, 0)


def test_toc():
    environment = Environment()
    environment.setvar(
        "mau.parser.header_anchor_function", lambda text, level: f"{text}-XXXXXX"
    )

    source = """
    = Header 1
    == Header 1.1
    = Header 2

    ::toc
    """

    parser = runner(source, environment)

    node_header_1_1 = Node(
        content=HeaderNodeContent(level=2, anchor="Header 1.1-XXXXXX"),
        info=NodeInfo(context=generate_context(2, 0)),
        children={
            "text": [
                Node(
                    content=TextNodeContent("Header 1.1"),
                    info=NodeInfo(context=generate_context(2, 3)),
                )
            ],
        },
    )

    node_header_1 = Node(
        content=HeaderNodeContent(level=1, anchor="Header 1-XXXXXX"),
        info=NodeInfo(context=generate_context(1, 0)),
        children={
            "text": [
                Node(
                    content=TextNodeContent("Header 1"),
                    info=NodeInfo(context=generate_context(1, 2)),
                )
            ],
        },
    )

    node_header_2 = Node(
        content=HeaderNodeContent(level=1, anchor="Header 2-XXXXXX"),
        info=NodeInfo(context=generate_context(3, 0)),
        children={
            "text": [
                Node(
                    content=TextNodeContent("Header 2"),
                    info=NodeInfo(context=generate_context(3, 2)),
                )
            ],
        },
    )

    node_toc_item_1_1 = Node(
        content=TocItemNodeContent(level=2, anchor="Header 1.1-XXXXXX"),
        info=NodeInfo(context=generate_context(2, 0)),
        children={
            "entries": [],
            "text": [
                Node(
                    content=TextNodeContent("Header 1.1"),
                    info=NodeInfo(context=generate_context(2, 3)),
                )
            ],
        },
    )

    node_toc_item_1 = Node(
        content=TocItemNodeContent(level=1, anchor="Header 1-XXXXXX"),
        info=NodeInfo(context=generate_context(1, 0)),
        children={
            "entries": [node_toc_item_1_1],
            "text": [
                Node(
                    content=TextNodeContent("Header 1"),
                    info=NodeInfo(context=generate_context(1, 2)),
                )
            ],
        },
    )

    node_toc_item_2 = Node(
        content=TocItemNodeContent(level=1, anchor="Header 2-XXXXXX"),
        info=NodeInfo(context=generate_context(3, 0)),
        children={
            "entries": [],
            "text": [
                Node(
                    content=TextNodeContent("Header 2"),
                    info=NodeInfo(context=generate_context(3, 2)),
                )
            ],
        },
    )

    node_toc = Node(
        content=TocNodeContent(),
        info=NodeInfo(context=generate_context(5, 0)),
        children={
            "nested_entries": [
                node_toc_item_1,
                node_toc_item_2,
            ],
            "plain_entries": [
                node_header_1,
                node_header_1_1,
                node_header_2,
            ],
        },
    )

    compare_nodes(
        parser.nodes,
        [
            node_header_1,
            node_header_1_1,
            node_header_2,
            node_toc,
        ],
    )


# def test_toc_inside_block():
#     environment = Environment()
#     environment.setvar(
#         "mau.parser.header_anchor_function", lambda text, level: f"{text}-XXXXXX"
#     )

#     source = """
#     ----
#     = Header 1
#     == Header 1.1
#     = Header 2

#     ::toc:
#     ----
#     """

#     parser = runner(source, environment)

#     assert parser.output == {
#         "content": ContainerNode(
#             children=[
#                 BlockNode(
#                     children=[
#                         HeaderNode(
#                             value=SentenceNode(children=[TextNode("Header 1")]),
#                             level="1",
#                             anchor="Header 1-XXXXXX",
#                         ),
#                         HeaderNode(
#                             value=SentenceNode(children=[TextNode("Header 1.1")]),
#                             level="2",
#                             anchor="Header 1.1-XXXXXX",
#                         ),
#                         HeaderNode(
#                             value=SentenceNode(children=[TextNode("Header 2")]),
#                             level="1",
#                             anchor="Header 2-XXXXXX",
#                         ),
#                         TocNode(
#                             children=[
#                                 TocEntryNode(
#                                     value=SentenceNode(children=[TextNode("Header 1")]),
#                                     anchor="Header 1-XXXXXX",
#                                     children=[
#                                         TocEntryNode(
#                                             value=SentenceNode(
#                                                 children=[TextNode("Header 1.1")]
#                                             ),
#                                             anchor="Header 1.1-XXXXXX",
#                                             children=[],
#                                         ),
#                                     ],
#                                 ),
#                                 TocEntryNode(
#                                     value=SentenceNode(children=[TextNode("Header 2")]),
#                                     anchor="Header 2-XXXXXX",
#                                     children=[],
#                                 ),
#                             ]
#                         ),
#                     ],
#                     preprocessor="none",
#                 )
#             ]
#         ),
#         "toc": ContainerNode(
#             children=[
#                 TocNode(
#                     children=[
#                         TocEntryNode(
#                             value=SentenceNode(children=[TextNode("Header 1")]),
#                             anchor="Header 1-XXXXXX",
#                             children=[
#                                 TocEntryNode(
#                                     value=SentenceNode(
#                                         children=[TextNode("Header 1.1")]
#                                     ),
#                                     anchor="Header 1.1-XXXXXX",
#                                     children=[],
#                                 ),
#                             ],
#                         ),
#                         TocEntryNode(
#                             value=SentenceNode(children=[TextNode("Header 2")]),
#                             anchor="Header 2-XXXXXX",
#                             children=[],
#                         ),
#                     ]
#                 )
#             ]
#         ),
#     }

#     toc_node = parser.output["toc"].children[0]

#     assert toc_node.parent == parser.output["toc"]
