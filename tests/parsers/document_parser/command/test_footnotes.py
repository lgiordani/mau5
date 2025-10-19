from unittest.mock import patch

from mau.lexers.document_lexer import DocumentLexer
from mau.nodes.footnotes import FootnotesItemNodeContent, FootnotesNodeContent
from mau.nodes.inline import TextNodeContent
from mau.nodes.lists import ListItemNodeContent, ListNodeContent
from mau.nodes.macros import MacroFootnoteNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.nodes.paragraph import ParagraphNodeContent
from mau.parsers.document_parser import DocumentParser
from mau.test_helpers import (
    compare_node,
    compare_nodes,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


@patch("mau.parsers.managers.footnotes_manager.default_footnote_unique_id")
def test_footnotes_in_paragraphs_are_detected(mock_footnote_unique_id):
    mock_footnote_unique_id.return_value = "XXYY"

    source = """
    This contains a footnote[footnote](somename).

    [somename, engine=footnote]
    ----
    Some text.
    ----
    """

    parser = runner(source)

    footnote_node = Node(
        content=FootnotesItemNodeContent("somename", "1", "XXYY"),
        info=NodeInfo(context=generate_context(4, 0, 6, 4)),
        children={
            "content": [
                Node(
                    content=ParagraphNodeContent(),
                    info=NodeInfo(context=generate_context(5, 0, 5, 10)),
                    children={
                        "content": [
                            Node(
                                content=TextNodeContent("Some text."),
                                info=NodeInfo(context=generate_context(5, 0, 5, 10)),
                            )
                        ]
                    },
                )
            ],
        },
    )

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(1, 0, 1, 45)),
                children={
                    "content": [
                        Node(
                            content=TextNodeContent("This contains a footnote"),
                            info=NodeInfo(context=generate_context(1, 0, 1, 24)),
                        ),
                        Node(
                            content=MacroFootnoteNodeContent("somename", "1", "XXYY"),
                            info=NodeInfo(context=generate_context(1, 24, 1, 44)),
                            children={"footnote": [footnote_node]},
                        ),
                        Node(
                            content=TextNodeContent("."),
                            info=NodeInfo(context=generate_context(1, 44, 1, 45)),
                        ),
                    ]
                },
            )
        ],
    )

    assert list(parser.footnotes_manager.data.keys()) == ["somename"]

    compare_node(parser.footnotes_manager.data["somename"], footnote_node)


@patch("mau.parsers.managers.footnotes_manager.default_footnote_unique_id")
def test_footnotes_in_lists_are_processed(mock_footnote_unique_id):
    mock_footnote_unique_id.return_value = "XXYY"

    source = """
    * This contains a footnote[footnote](somename).

    [somename, engine=footnote]
    ----
    Some text.
    ----
    """

    parser = runner(source)

    footnote_node = Node(
        content=FootnotesItemNodeContent("somename", "1", "XXYY"),
        info=NodeInfo(context=generate_context(4, 0, 6, 4)),
        children={
            "content": [
                Node(
                    content=ParagraphNodeContent(),
                    info=NodeInfo(context=generate_context(5, 0, 5, 10)),
                    children={
                        "content": [
                            Node(
                                content=TextNodeContent("Some text."),
                                info=NodeInfo(context=generate_context(5, 0, 5, 10)),
                            )
                        ]
                    },
                )
            ],
        },
    )

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=ListNodeContent(ordered=False, main_node=True),
                info=NodeInfo(context=generate_context(1, 0, 1, 47)),
                children={
                    "nodes": [
                        Node(
                            content=ListItemNodeContent("1"),
                            info=NodeInfo(context=generate_context(1, 0, 1, 47)),
                            children={
                                "text": [
                                    Node(
                                        content=TextNodeContent(
                                            "This contains a footnote"
                                        ),
                                        info=NodeInfo(
                                            context=generate_context(1, 2, 1, 26)
                                        ),
                                    ),
                                    Node(
                                        content=MacroFootnoteNodeContent(
                                            "somename", "1", "XXYY"
                                        ),
                                        info=NodeInfo(
                                            context=generate_context(1, 26, 1, 46)
                                        ),
                                        children={"footnote": [footnote_node]},
                                    ),
                                    Node(
                                        content=TextNodeContent("."),
                                        info=NodeInfo(
                                            context=generate_context(1, 46, 1, 47)
                                        ),
                                    ),
                                ]
                            },
                        )
                    ]
                },
            )
        ],
    )

    assert list(parser.footnotes_manager.data.keys()) == ["somename"]

    compare_node(parser.footnotes_manager.data["somename"], footnote_node)


@patch("mau.parsers.managers.footnotes_manager.default_footnote_unique_id")
def test_footnotes_command(mock_footnote_unique_id):
    mock_footnote_unique_id.return_value = "XXYY"

    source = """
    This contains a footnote[footnote](somename).

    [somename, engine=footnote]
    ----
    Some text.
    ----

    ::footnotes
    """

    parser = runner(source)

    footnote_node = Node(
        content=FootnotesItemNodeContent("somename", "1", "XXYY"),
        info=NodeInfo(context=generate_context(4, 0, 6, 4)),
        children={
            "content": [
                Node(
                    content=ParagraphNodeContent(),
                    info=NodeInfo(context=generate_context(5, 0, 5, 10)),
                    children={
                        "content": [
                            Node(
                                content=TextNodeContent("Some text."),
                                info=NodeInfo(context=generate_context(5, 0, 5, 10)),
                            )
                        ]
                    },
                )
            ],
        },
    )

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(1, 0, 1, 45)),
                children={
                    "content": [
                        Node(
                            content=TextNodeContent("This contains a footnote"),
                            info=NodeInfo(context=generate_context(1, 0, 1, 24)),
                        ),
                        Node(
                            content=MacroFootnoteNodeContent("somename", "1", "XXYY"),
                            info=NodeInfo(context=generate_context(1, 24, 1, 44)),
                            children={"footnote": [footnote_node]},
                        ),
                        Node(
                            content=TextNodeContent("."),
                            info=NodeInfo(context=generate_context(1, 44, 1, 45)),
                        ),
                    ]
                },
            ),
            Node(
                content=FootnotesNodeContent(),
                info=NodeInfo(context=generate_context(8, 0, 8, 11)),
                children={"entries": [footnote_node]},
            ),
        ],
    )

    assert list(parser.footnotes_manager.data.keys()) == ["somename"]

    compare_node(parser.footnotes_manager.data["somename"], footnote_node)
