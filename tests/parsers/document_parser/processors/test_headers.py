from mau.environment.environment import Environment
from mau.lexers.document_lexer.lexer import DocumentLexer
from mau.nodes.headers import HeaderNodeContent
from mau.nodes.inline import SentenceNodeContent, TextNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.arguments_parser.parser import Arguments
from mau.parsers.document_parser.parser import DocumentParser
from mau.parsers.document_parser.processors.header import header_processor
from mau.test_helpers import (
    compare_nodes,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


# @patch("mau.parsers.toc.hashlib.md5")
# def test_default_header_anchor_function(mock_md5):
#     mock_md5().hexdigest.return_value = "XXYY"

#     assert header_anchor("Some Words 1234 56", "1") == "some-words-1234-56-XXYY"


# @patch("mau.parsers.toc.hashlib.md5")
# def test_default_header_anchor_function_multiple_spaces(mock_md5):
#     mock_md5().hexdigest.return_value = "XXYY"

#     assert (
#         header_anchor("Some    Words     1234    56", "1") == "some-words-1234-56-XXYY"
#     )


# @patch("mau.parsers.toc.hashlib.md5")
# def test_default_header_anchor_function_filter_characters(mock_md5):
#     mock_md5().hexdigest.return_value = "XXYY"

#     assert header_anchor("Some #Words @ 12!34 56", "1") == "some-words-1234-56-XXYY"


# def test_custom_header_anchor_function():
#     source = """
#     = Title of the section
#     """

#     environment = Environment()
#     environment.setvar(
#         "mau.parser.header_anchor_function", lambda text, level: "XXXXXY"
#     )

#     assert runner(source, environment).nodes == [
#         HeaderNode(
#             value=SentenceNode(children=[TextNode("Title of the section")]),
#             level="1",
#             anchor="XXXXXY",
#         )
#     ]


def test_header_level_1():
    environment = Environment()
    environment.setvar(
        "mau.parser.header_anchor_function", lambda text, level: "XXXXXY"
    )

    source = "= Title of the section"

    parser: DocumentParser = init_parser(source, environment)
    header_processor(parser)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=HeaderNodeContent(1, "XXXXXY"),
                info=NodeInfo(context=generate_context(0, 0)),
                children={
                    "text": [
                        Node(
                            content=SentenceNodeContent(),
                            info=NodeInfo(context=generate_context(0, 2)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent("Title of the section"),
                                        info=NodeInfo(context=generate_context(0, 2)),
                                    )
                                ]
                            },
                        )
                    ],
                },
            )
        ],
    )


def test_header_level_3():
    environment = Environment()
    environment.setvar(
        "mau.parser.header_anchor_function", lambda text, level: "XXXXXY"
    )

    source = "=== Title of a subsection"

    parser: DocumentParser = init_parser(source, environment)
    header_processor(parser)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=HeaderNodeContent(3, "XXXXXY"),
                info=NodeInfo(context=generate_context(0, 0)),
                children={
                    "text": [
                        Node(
                            content=SentenceNodeContent(),
                            info=NodeInfo(context=generate_context(0, 4)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent(
                                            "Title of a subsection"
                                        ),
                                        info=NodeInfo(context=generate_context(0, 4)),
                                    )
                                ]
                            },
                        )
                    ],
                },
            )
        ],
    )


# def test_parse_collect_headers():
#     environment = Environment()
#     environment.setvar(
#         "mau.parser.header_anchor_function", lambda text, level: f"{text}-XXXXXX"
#     )

#     source = """
#     = Header 1
#     == Header 1.1
#     == Header 1.2
#     = Header 2
#     == Header 2.1
#     === Header 2.1.1
#     """

#     parser = runner(source, environment)

#     assert parser.nodes == [
#         HeaderNode(
#             value=SentenceNode(children=[TextNode("Header 1")]),
#             level="1",
#             anchor="Header 1-XXXXXX",
#         ),
#         HeaderNode(
#             value=SentenceNode(children=[TextNode("Header 1.1")]),
#             level="2",
#             anchor="Header 1.1-XXXXXX",
#         ),
#         HeaderNode(
#             value=SentenceNode(children=[TextNode("Header 1.2")]),
#             level="2",
#             anchor="Header 1.2-XXXXXX",
#         ),
#         HeaderNode(
#             value=SentenceNode(children=[TextNode("Header 2")]),
#             level="1",
#             anchor="Header 2-XXXXXX",
#         ),
#         HeaderNode(
#             value=SentenceNode(children=[TextNode("Header 2.1")]),
#             level="2",
#             anchor="Header 2.1-XXXXXX",
#         ),
#         HeaderNode(
#             value=SentenceNode(children=[TextNode("Header 2.1.1")]),
#             level="3",
#             anchor="Header 2.1.1-XXXXXX",
#         ),
#     ]

#     assert parser.toc_manager.headers == [
#         HeaderNode(
#             value=SentenceNode(children=[TextNode("Header 1")]),
#             level="1",
#             anchor="Header 1-XXXXXX",
#         ),
#         HeaderNode(
#             value=SentenceNode(children=[TextNode("Header 1.1")]),
#             level="2",
#             anchor="Header 1.1-XXXXXX",
#         ),
#         HeaderNode(
#             value=SentenceNode(children=[TextNode("Header 1.2")]),
#             level="2",
#             anchor="Header 1.2-XXXXXX",
#         ),
#         HeaderNode(
#             value=SentenceNode(children=[TextNode("Header 2")]),
#             level="1",
#             anchor="Header 2-XXXXXX",
#         ),
#         HeaderNode(
#             value=SentenceNode(children=[TextNode("Header 2.1")]),
#             level="2",
#             anchor="Header 2.1-XXXXXX",
#         ),
#         HeaderNode(
#             value=SentenceNode(children=[TextNode("Header 2.1.1")]),
#             level="3",
#             anchor="Header 2.1.1-XXXXXX",
#         ),
#     ]


def test_header_attributes():
    environment = Environment()
    environment.setvar(
        "mau.parser.header_anchor_function", lambda text, level: "XXXXXY"
    )

    source = "= Title of the section"

    parser: DocumentParser = init_parser(source, environment)
    parser.arguments_buffer.push(
        Arguments(
            unnamed_args=["arg1"],
            named_args={"key1": "value1"},
            tags=["tag1"],
            subtype="subtype1",
        )
    )

    header_processor(parser)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=HeaderNodeContent(1, "XXXXXY"),
                info=NodeInfo(
                    context=generate_context(0, 0),
                    unnamed_args=["arg1"],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
                children={
                    "text": [
                        Node(
                            content=SentenceNodeContent(),
                            info=NodeInfo(context=generate_context(0, 2)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent("Title of the section"),
                                        info=NodeInfo(context=generate_context(0, 2)),
                                    )
                                ]
                            },
                        )
                    ],
                },
            )
        ],
    )


def test_header_attributes_can_overwrite_anchor():
    source = "= Header"

    parser: DocumentParser = init_parser(source)
    parser.arguments_buffer.push(
        Arguments(
            unnamed_args=["arg1"],
            named_args={"anchor": "someheader"},
            tags=["tag1"],
            subtype="subtype1",
        )
    )

    header_processor(parser)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=HeaderNodeContent(1, "someheader"),
                info=NodeInfo(
                    context=generate_context(0, 0),
                    unnamed_args=["arg1"],
                    named_args={},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
                children={
                    "text": [
                        Node(
                            content=SentenceNodeContent(),
                            info=NodeInfo(context=generate_context(0, 2)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent("Header"),
                                        info=NodeInfo(context=generate_context(0, 2)),
                                    )
                                ]
                            },
                        )
                    ],
                },
            )
        ],
    )


# def test_header_ignore_title():
#     environment = Environment()
#     environment.setvar(
#         "mau.parser.header_anchor_function", lambda text, level: "XXXXXY"
#     )

#     source = """
#     . A title
#     = Title of the section
#     """

#     parser = runner(source, environment)

#     compare_nodes(
#         parser.nodes,
#         [
#             Node(
#                 content=HeaderNodeContent(1, "XXXXXY"),
#                 info=NodeInfo(context=generate_context(2, 0)),
#                 children={
#                     "entries": [],
#                     "text": [
#                         Node(
#                             content=SentenceNodeContent(),
#                             info=NodeInfo(context=generate_context(2, 2)),
#                             children={
#                                 "content": [
#                                     Node(
#                                         content=TextNodeContent("Title of the section"),
#                                         info=NodeInfo(context=generate_context(2, 2)),
#                                     )
#                                 ]
#                             },
#                         )
#                     ],
#                 },
#             )
#         ],
#     )


# def test_header_with_id_is_stored():
#     environment = Environment()
#     environment.setvar(
#         "mau.parser.header_anchor_function", lambda text, level: f"{text}-XXXXXX"
#     )

#     source = """
#     [arg1,id=someid,key1=value1]
#     = Header
#     """

#     node = HeaderNode(
#         value=SentenceNode(children=[TextNode("Header")]),
#         level="1",
#         anchor="Header-XXXXXX",
#         args=["arg1"],
#         kwargs={"id": "someid", "key1": "value1"},
#     )

#     parser = runner(source, environment)

#     assert parser.nodes == [node]
#     assert parser.internal_links_manager.headers == {"someid": node}


# def test_header_with_duplicate_id():
#     source = """
#     [arg1,id=someid,key1=value1]
#     = Header

#     [id=someid]
#     = Another Header
#     """

#     with pytest.raises(MauErrorException):
#         runner(source)


# def test_single_tag_header():
#     environment = Environment()
#     environment.setvar(
#         "mau.parser.header_anchor_function", lambda text, level: f"{text}-XXXXXX"
#     )

#     source = """
#     [arg1, #tag1, key1=value1]
#     = Header
#     """

#     assert runner(source, environment).nodes == [
#         HeaderNode(
#             value=SentenceNode(children=[TextNode("Header")]),
#             level="1",
#             anchor="Header-XXXXXX",
#             args=["arg1"],
#             kwargs={"key1": "value1"},
#             tags=["tag1"],
#         ),
#     ]
