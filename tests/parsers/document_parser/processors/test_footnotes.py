from unittest.mock import patch

from mau.lexers.document_lexer.lexer import DocumentLexer
from mau.nodes.footnotes import FootnoteNodeContent, FootnotesListNodeContent
from mau.nodes.inline import TextNodeContent
from mau.nodes.lists import ListItemNodeContent, ListNodeContent
from mau.nodes.macros import MacroFootnoteNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.nodes.paragraph import ParagraphNodeContent
from mau.parsers.document_parser.parser import DocumentParser
from mau.test_helpers import (
    compare_node,
    compare_nodes,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


@patch(
    "mau.parsers.document_parser.managers.footnotes_manager.default_footnote_unique_id"
)
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
        content=FootnoteNodeContent("somename", "1", "XXYY"),
        info=NodeInfo(context=generate_context(4, 0)),
        children={
            "content": [
                Node(
                    content=ParagraphNodeContent(),
                    info=NodeInfo(context=generate_context(5, 0)),
                    children={
                        "content": [
                            Node(
                                content=TextNodeContent("Some text."),
                                info=NodeInfo(context=generate_context(5, 0)),
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
                info=NodeInfo(context=generate_context(1, 0)),
                children={
                    "content": [
                        Node(
                            content=TextNodeContent("This contains a footnote"),
                            info=NodeInfo(context=generate_context(1, 0)),
                        ),
                        Node(
                            content=MacroFootnoteNodeContent("somename", "1", "XXYY"),
                            info=NodeInfo(context=generate_context(1, 24)),
                            children={"footnote": [footnote_node]},
                        ),
                        Node(
                            content=TextNodeContent("."),
                            info=NodeInfo(context=generate_context(1, 44)),
                        ),
                    ]
                },
            )
        ],
    )

    assert list(parser.footnotes_manager.data.keys()) == ["somename"]

    compare_node(parser.footnotes_manager.data["somename"], footnote_node)


@patch(
    "mau.parsers.document_parser.managers.footnotes_manager.default_footnote_unique_id"
)
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
        content=FootnoteNodeContent("somename", "1", "XXYY"),
        info=NodeInfo(context=generate_context(4, 0)),
        children={
            "content": [
                Node(
                    content=ParagraphNodeContent(),
                    info=NodeInfo(context=generate_context(5, 0)),
                    children={
                        "content": [
                            Node(
                                content=TextNodeContent("Some text."),
                                info=NodeInfo(context=generate_context(5, 0)),
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
                info=NodeInfo(context=generate_context(1, 0)),
                children={
                    "nodes": [
                        Node(
                            content=ListItemNodeContent("1"),
                            info=NodeInfo(context=generate_context(1, 0)),
                            children={
                                "text": [
                                    Node(
                                        content=TextNodeContent(
                                            "This contains a footnote"
                                        ),
                                        info=NodeInfo(context=generate_context(1, 2)),
                                    ),
                                    Node(
                                        content=MacroFootnoteNodeContent(
                                            "somename", "1", "XXYY"
                                        ),
                                        info=NodeInfo(context=generate_context(1, 26)),
                                        children={"footnote": [footnote_node]},
                                    ),
                                    Node(
                                        content=TextNodeContent("."),
                                        info=NodeInfo(context=generate_context(1, 46)),
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


@patch(
    "mau.parsers.document_parser.managers.footnotes_manager.default_footnote_unique_id"
)
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
        content=FootnoteNodeContent("somename", "1", "XXYY"),
        info=NodeInfo(context=generate_context(4, 0)),
        children={
            "content": [
                Node(
                    content=ParagraphNodeContent(),
                    info=NodeInfo(context=generate_context(5, 0)),
                    children={
                        "content": [
                            Node(
                                content=TextNodeContent("Some text."),
                                info=NodeInfo(context=generate_context(5, 0)),
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
                info=NodeInfo(context=generate_context(1, 0)),
                children={
                    "content": [
                        Node(
                            content=TextNodeContent("This contains a footnote"),
                            info=NodeInfo(context=generate_context(1, 0)),
                        ),
                        Node(
                            content=MacroFootnoteNodeContent("somename", "1", "XXYY"),
                            info=NodeInfo(context=generate_context(1, 24)),
                            children={"footnote": [footnote_node]},
                        ),
                        Node(
                            content=TextNodeContent("."),
                            info=NodeInfo(context=generate_context(1, 44)),
                        ),
                    ]
                },
            ),
            Node(
                content=FootnotesListNodeContent(),
                info=NodeInfo(context=generate_context(8, 0)),
                children={"entries": [footnote_node]},
            ),
        ],
    )

    assert list(parser.footnotes_manager.data.keys()) == ["somename"]

    compare_node(parser.footnotes_manager.data["somename"], footnote_node)
