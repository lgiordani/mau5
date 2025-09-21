from unittest.mock import patch

import pytest

from mau.lexers.document_lexer.lexer import DocumentLexer
from mau.nodes.block import BlockNodeContent
from mau.nodes.headers import HeaderNodeContent
from mau.nodes.inline import SentenceNodeContent, TextNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.nodes.paragraph import ParagraphNodeContent
from mau.nodes.toc import TocItemNodeContent, TocNodeContent
from mau.parsers.base_parser.parser import MauParserException
from mau.parsers.document_parser.parser import DocumentParser
from mau.test_helpers import (
    compare_nodes,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


@patch("mau.parsers.document_parser.parser.header_anchor")
def test_mau_engine_doesnt_add_headers_to_the_global_toc(mock_header_anchor):
    mock_header_anchor.return_value = "XXYY"

    source = """
    = Global header

    [engine=mau]
    ----
    = Block header
    ----
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=HeaderNodeContent(1, "XXYY"),
                info=NodeInfo(context=generate_context(1, 0)),
                children={
                    "text": [
                        Node(
                            content=TextNodeContent("Global header"),
                            info=NodeInfo(context=generate_context(1, 2)),
                        )
                    ],
                },
            ),
            Node(
                content=BlockNodeContent(
                    classes=[],
                    engine="mau",
                    preprocessor=None,
                ),
                info=NodeInfo(context=generate_context(4, 0)),
                children={
                    "content": [
                        Node(
                            content=HeaderNodeContent(1, "XXYY"),
                            info=NodeInfo(context=generate_context(5, 0)),
                            children={
                                "text": [
                                    Node(
                                        content=TextNodeContent("Block header"),
                                        info=NodeInfo(context=generate_context(5, 2)),
                                    )
                                ],
                            },
                        ),
                    ]
                },
            ),
        ],
    )

    compare_nodes(
        parser.toc_manager.headers,
        [
            Node(
                content=HeaderNodeContent(1, "XXYY"),
                info=NodeInfo(context=generate_context(1, 0)),
                children={
                    "text": [
                        Node(
                            content=TextNodeContent("Global header"),
                            info=NodeInfo(context=generate_context(1, 2)),
                        )
                    ]
                },
            ),
        ],
    )


@patch("mau.parsers.document_parser.parser.header_anchor")
def test_engine_mau_multiple_blocks_are_independent(mock_header_anchor):
    mock_header_anchor.return_value = "XXYY"

    source = """
    = Global header

    [engine=mau]
    ----
    = Block header 1
    ----

    [engine=mau]
    ----
    = Block header 2
    ----
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=HeaderNodeContent(1, "XXYY"),
                info=NodeInfo(context=generate_context(1, 0)),
                children={
                    "text": [
                        Node(
                            content=TextNodeContent("Global header"),
                            info=NodeInfo(context=generate_context(1, 2)),
                        )
                    ],
                },
            ),
            Node(
                content=BlockNodeContent(
                    classes=[],
                    engine="mau",
                    preprocessor=None,
                ),
                info=NodeInfo(context=generate_context(4, 0)),
                children={
                    "content": [
                        Node(
                            content=HeaderNodeContent(1, "XXYY"),
                            info=NodeInfo(context=generate_context(5, 0)),
                            children={
                                "text": [
                                    Node(
                                        content=TextNodeContent("Block header 1"),
                                        info=NodeInfo(context=generate_context(5, 2)),
                                    )
                                ],
                            },
                        ),
                    ]
                },
            ),
            Node(
                content=BlockNodeContent(
                    classes=[],
                    engine="mau",
                    preprocessor=None,
                ),
                info=NodeInfo(context=generate_context(9, 0)),
                children={
                    "content": [
                        Node(
                            content=HeaderNodeContent(1, "XXYY"),
                            info=NodeInfo(context=generate_context(10, 0)),
                            children={
                                "text": [
                                    Node(
                                        content=TextNodeContent("Block header 2"),
                                        info=NodeInfo(context=generate_context(10, 2)),
                                    )
                                ],
                            },
                        ),
                    ]
                },
            ),
        ],
    )

    compare_nodes(
        parser.toc_manager.headers,
        [
            Node(
                content=HeaderNodeContent(1, "XXYY"),
                info=NodeInfo(context=generate_context(1, 0)),
                children={
                    "text": [
                        Node(
                            content=TextNodeContent("Global header"),
                            info=NodeInfo(context=generate_context(1, 2)),
                        )
                    ],
                },
            ),
        ],
    )


@patch("mau.parsers.document_parser.parser.header_anchor")
def test_engine_mau_toc(mock_header_anchor):
    mock_header_anchor.return_value = "XXYY"

    source = """
    = Global header

    [engine=mau]
    ----
    = Block header

    ::toc
    ----

    ::toc
    """

    parser = runner(source)

    # This is the global header.
    global_header_node = Node(
        content=HeaderNodeContent(1, "XXYY"),
        info=NodeInfo(context=generate_context(1, 0)),
        children={
            "text": [
                Node(
                    content=TextNodeContent("Global header"),
                    info=NodeInfo(context=generate_context(1, 2)),
                )
            ],
        },
    )

    # This is the global header ToC item.
    global_header_toc_item_node = Node(
        content=TocItemNodeContent(1, "XXYY"),
        info=NodeInfo(context=generate_context(1, 0)),
        children={
            "entries": [],
            "text": [
                Node(
                    content=TextNodeContent("Global header"),
                    info=NodeInfo(context=generate_context(1, 2)),
                )
            ],
        },
    )

    # This is the block header.
    block_header_node = Node(
        content=HeaderNodeContent(1, "XXYY"),
        info=NodeInfo(context=generate_context(5, 0)),
        children={
            "text": [
                Node(
                    content=TextNodeContent("Block header"),
                    info=NodeInfo(context=generate_context(5, 2)),
                )
            ],
        },
    )

    # This is the block header ToC item.
    block_header_toc_item_node = Node(
        content=TocItemNodeContent(1, "XXYY"),
        info=NodeInfo(context=generate_context(5, 0)),
        children={
            "entries": [],
            "text": [
                Node(
                    content=TextNodeContent("Block header"),
                    info=NodeInfo(context=generate_context(5, 2)),
                )
            ],
        },
    )

    compare_nodes(
        parser.nodes,
        [
            # This is the global header.
            global_header_node,
            # This is the content of the block.
            Node(
                content=BlockNodeContent(
                    classes=[],
                    engine="mau",
                    preprocessor=None,
                ),
                info=NodeInfo(context=generate_context(4, 0)),
                children={
                    "content": [
                        # This is the block header.
                        block_header_node,
                        # This is the block ToC.
                        Node(
                            content=TocNodeContent(),
                            info=NodeInfo(context=generate_context(7, 0)),
                            children={
                                "nested_entries": [block_header_toc_item_node],
                                "plain_entries": [block_header_node],
                            },
                        ),
                    ]
                },
            ),
            # This is the global ToC
            Node(
                content=TocNodeContent(),
                info=NodeInfo(context=generate_context(10, 0)),
                children={
                    "nested_entries": [global_header_toc_item_node],
                    "plain_entries": [global_header_node],
                },
            ),
        ],
    )


def test_block_mau_cannot_see_external_variables():
    source = """
    :answer:42

    [engine=mau]
    ----
    The answer is {answer}.
    ----
    """

    with pytest.raises(MauParserException):
        assert runner(source)


def test_block_mau_can_see_internal_variables():
    source = """
    [engine=mau]
    ----
    :answer:42

    The answer is {answer}.
    ----
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=BlockNodeContent(
                    classes=[],
                    engine="mau",
                    preprocessor=None,
                ),
                info=NodeInfo(context=generate_context(2, 0)),
                children={
                    "content": [
                        Node(
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent("The answer is 42."),
                                        info=NodeInfo(context=generate_context(5, 0)),
                                    ),
                                ]
                            },
                            content=ParagraphNodeContent(),
                            info=NodeInfo(context=generate_context(5, 0)),
                        ),
                    ]
                },
            )
        ],
    )
