from unittest.mock import patch

import pytest

from mau.lexers.document_lexer import DocumentLexer
from mau.nodes.block import BlockNodeContent
from mau.nodes.headers import HeaderNodeContent
from mau.nodes.inline import TextNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.nodes.paragraph import ParagraphNodeContent
from mau.nodes.command import TocItemNodeContent, TocNodeContent
from mau.parsers.base_parser import MauParserException
from mau.parsers.document_parser import DocumentParser
from mau.test_helpers import (
    compare_nodes,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


@patch("mau.parsers.managers.toc_manager.default_header_internal_id")
def test_block_isolation_doesnt_add_headers_to_the_global_toc(mock_header_internal_id):
    mock_header_internal_id.return_value = "XXYY"

    source = """
    = Global header

    [isolate=true]
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
                info=NodeInfo(context=generate_context(1, 0, 1, 15)),
                children={
                    "text": [
                        Node(
                            content=TextNodeContent("Global header"),
                            info=NodeInfo(context=generate_context(1, 2, 1, 15)),
                        )
                    ],
                },
            ),
            Node(
                content=BlockNodeContent(
                    classes=[],
                    engine="default",
                    preprocessor=None,
                ),
                info=NodeInfo(
                    context=generate_context(4, 0, 6, 4),
                    named_args={"isolate": "true"},
                ),
                children={
                    "content": [
                        Node(
                            content=HeaderNodeContent(1, "XXYY"),
                            info=NodeInfo(context=generate_context(5, 0, 5, 14)),
                            children={
                                "text": [
                                    Node(
                                        content=TextNodeContent("Block header"),
                                        info=NodeInfo(
                                            context=generate_context(5, 2, 5, 14)
                                        ),
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
                info=NodeInfo(context=generate_context(1, 0, 1, 15)),
                children={
                    "text": [
                        Node(
                            content=TextNodeContent("Global header"),
                            info=NodeInfo(context=generate_context(1, 2, 1, 15)),
                        )
                    ]
                },
            ),
        ],
    )


@patch("mau.parsers.managers.toc_manager.default_header_internal_id")
def test_block_isolation_multiple_blocks_are_independent(mock_header_internal_id):
    mock_header_internal_id.return_value = "XXYY"

    source = """
    = Global header

    [isolate=true]
    ----
    = Block header 1
    ----

    [isolate=true]
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
                info=NodeInfo(context=generate_context(1, 0, 1, 15)),
                children={
                    "text": [
                        Node(
                            content=TextNodeContent("Global header"),
                            info=NodeInfo(context=generate_context(1, 2, 1, 15)),
                        )
                    ],
                },
            ),
            Node(
                content=BlockNodeContent(
                    classes=[],
                    engine="default",
                    preprocessor=None,
                ),
                info=NodeInfo(
                    context=generate_context(4, 0, 6, 4),
                    named_args={"isolate": "true"},
                ),
                children={
                    "content": [
                        Node(
                            content=HeaderNodeContent(1, "XXYY"),
                            info=NodeInfo(context=generate_context(5, 0, 5, 16)),
                            children={
                                "text": [
                                    Node(
                                        content=TextNodeContent("Block header 1"),
                                        info=NodeInfo(
                                            context=generate_context(5, 2, 5, 16)
                                        ),
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
                    engine="default",
                    preprocessor=None,
                ),
                info=NodeInfo(
                    context=generate_context(9, 0, 11, 4),
                    named_args={"isolate": "true"},
                ),
                children={
                    "content": [
                        Node(
                            content=HeaderNodeContent(1, "XXYY"),
                            info=NodeInfo(context=generate_context(10, 0, 10, 16)),
                            children={
                                "text": [
                                    Node(
                                        content=TextNodeContent("Block header 2"),
                                        info=NodeInfo(
                                            context=generate_context(10, 2, 10, 16)
                                        ),
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
                info=NodeInfo(context=generate_context(1, 0, 1, 15)),
                children={
                    "text": [
                        Node(
                            content=TextNodeContent("Global header"),
                            info=NodeInfo(context=generate_context(1, 2, 1, 15)),
                        )
                    ],
                },
            ),
        ],
    )


@patch("mau.parsers.managers.toc_manager.default_header_internal_id")
def test_block_isolation_toc(mock_header_internal_id):
    mock_header_internal_id.return_value = "XXYY"

    source = """
    = Global header

    [isolate=true]
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
        info=NodeInfo(context=generate_context(1, 0, 1, 15)),
        children={
            "text": [
                Node(
                    content=TextNodeContent("Global header"),
                    info=NodeInfo(context=generate_context(1, 2, 1, 15)),
                )
            ],
        },
    )

    # This is the global header ToC item.
    global_header_toc_item_node = Node(
        content=TocItemNodeContent(1, "XXYY"),
        info=NodeInfo(context=generate_context(1, 0, 1, 15)),
        children={
            "entries": [],
            "text": [
                Node(
                    content=TextNodeContent("Global header"),
                    info=NodeInfo(context=generate_context(1, 2, 1, 15)),
                )
            ],
        },
    )

    # This is the block header.
    block_header_node = Node(
        content=HeaderNodeContent(1, "XXYY"),
        info=NodeInfo(context=generate_context(5, 0, 5, 14)),
        children={
            "text": [
                Node(
                    content=TextNodeContent("Block header"),
                    info=NodeInfo(context=generate_context(5, 2, 5, 14)),
                )
            ],
        },
    )

    # This is the block header ToC item.
    block_header_toc_item_node = Node(
        content=TocItemNodeContent(1, "XXYY"),
        info=NodeInfo(context=generate_context(5, 0, 5, 14)),
        children={
            "entries": [],
            "text": [
                Node(
                    content=TextNodeContent("Block header"),
                    info=NodeInfo(context=generate_context(5, 2, 5, 14)),
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
                    engine="default",
                    preprocessor=None,
                ),
                info=NodeInfo(
                    context=generate_context(4, 0, 8, 4),
                    named_args={"isolate": "true"},
                ),
                children={
                    "content": [
                        # This is the block header.
                        block_header_node,
                        # This is the block ToC.
                        Node(
                            content=TocNodeContent(),
                            info=NodeInfo(context=generate_context(7, 0, 7, 5)),
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
                info=NodeInfo(context=generate_context(10, 0, 10, 5)),
                children={
                    "nested_entries": [global_header_toc_item_node],
                    "plain_entries": [global_header_node],
                },
            ),
        ],
    )


def test_block_isolation_cannot_see_external_variables():
    source = """
    :answer:42

    [isolate=true]
    ----
    The answer is {answer}.
    ----
    """

    with pytest.raises(MauParserException):
        assert runner(source)


def test_block_isolation_can_see_internal_variables():
    source = """
    [isolate=true]
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
                    engine="default",
                    preprocessor=None,
                ),
                info=NodeInfo(
                    context=generate_context(2, 0, 6, 4),
                    named_args={"isolate": "true"},
                ),
                children={
                    "content": [
                        Node(
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent("The answer is 42."),
                                        info=NodeInfo(
                                            context=generate_context(5, 0, 5, 17)
                                        ),
                                    ),
                                ]
                            },
                            content=ParagraphNodeContent(),
                            info=NodeInfo(context=generate_context(5, 0, 5, 23)),
                        ),
                    ]
                },
            )
        ],
    )
