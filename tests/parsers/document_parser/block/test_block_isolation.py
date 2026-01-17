from unittest.mock import patch

import pytest

from mau.lexers.document_lexer import DocumentLexer
from mau.nodes.block import BlockNode
from mau.nodes.commands import TocItemNode, TocNode
from mau.nodes.headers import HeaderNode
from mau.nodes.inline import TextNode
from mau.nodes.node import Node, NodeInfo
from mau.nodes.paragraph import ParagraphLineNode, ParagraphNode
from mau.parsers.base_parser import MauParserException
from mau.parsers.document_parser import DocumentParser
from mau.test_helpers import (
    compare_asdict_list,
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

    compare_asdict_list(
        parser.nodes,
        [
            HeaderNode(
                1,
                "XXYY",
                content=[
                    TextNode(
                        "Global header",
                        info=NodeInfo(context=generate_context(1, 2, 1, 15)),
                    )
                ],
                info=NodeInfo(context=generate_context(1, 0, 1, 15)),
            ),
            BlockNode(
                classes=[],
                engine="default",
                content=[
                    HeaderNode(
                        1,
                        "XXYY",
                        content=[
                            TextNode(
                                "Block header",
                                info=NodeInfo(context=generate_context(5, 2, 5, 14)),
                            )
                        ],
                        info=NodeInfo(context=generate_context(5, 0, 5, 14)),
                    ),
                ],
                info=NodeInfo(
                    context=generate_context(4, 0, 6, 4),
                    named_args={"isolate": "true"},
                ),
            ),
        ],
    )

    compare_asdict_list(
        parser.toc_manager.headers,
        [
            HeaderNode(
                1,
                "XXYY",
                content=[
                    TextNode(
                        "Global header",
                        info=NodeInfo(context=generate_context(1, 2, 1, 15)),
                    )
                ],
                info=NodeInfo(
                    context=generate_context(1, 0, 1, 15),
                ),
            )
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

    compare_asdict_list(
        parser.nodes,
        [
            HeaderNode(
                1,
                "XXYY",
                content=[
                    TextNode(
                        "Global header",
                        info=NodeInfo(context=generate_context(1, 2, 1, 15)),
                    )
                ],
                info=NodeInfo(context=generate_context(1, 0, 1, 15)),
            ),
            BlockNode(
                classes=[],
                engine="default",
                content=[
                    HeaderNode(
                        1,
                        "XXYY",
                        content=[
                            TextNode(
                                "Block header 1",
                                info=NodeInfo(context=generate_context(5, 2, 5, 16)),
                            )
                        ],
                        info=NodeInfo(context=generate_context(5, 0, 5, 16)),
                    ),
                ],
                info=NodeInfo(
                    context=generate_context(4, 0, 6, 4),
                    named_args={"isolate": "true"},
                ),
            ),
            BlockNode(
                classes=[],
                engine="default",
                content=[
                    HeaderNode(
                        1,
                        "XXYY",
                        content=[
                            TextNode(
                                "Block header 2",
                                info=NodeInfo(context=generate_context(10, 2, 10, 16)),
                            )
                        ],
                        info=NodeInfo(context=generate_context(10, 0, 10, 16)),
                    ),
                ],
                info=NodeInfo(
                    context=generate_context(9, 0, 11, 4),
                    named_args={"isolate": "true"},
                ),
            ),
        ],
    )

    compare_asdict_list(
        parser.toc_manager.headers,
        [
            HeaderNode(
                1,
                "XXYY",
                content=[
                    TextNode(
                        "Global header",
                        info=NodeInfo(context=generate_context(1, 2, 1, 15)),
                    )
                ],
                info=NodeInfo(
                    context=generate_context(1, 0, 1, 15),
                ),
            )
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

    # This is the global header node.
    global_header_node = HeaderNode(
        1,
        "XXYY",
        content=[
            TextNode(
                "Global header",
                info=NodeInfo(context=generate_context(1, 2, 1, 15)),
            )
        ],
        info=NodeInfo(context=generate_context(1, 0, 1, 15)),
    )

    # This is the global header ToC item data.
    global_header_toc_item_node = TocItemNode(header=global_header_node)

    # This is the block header node.
    block_header_node = HeaderNode(
        1,
        "XXYY",
        content=[
            TextNode(
                "Block header",
                info=NodeInfo(context=generate_context(5, 2, 5, 14)),
            )
        ],
        info=NodeInfo(context=generate_context(5, 0, 5, 14)),
    )

    # This is the block header ToC item data.
    block_header_toc_item_node = TocItemNode(header=block_header_node)

    compare_asdict_list(
        parser.nodes,
        [
            # This is the global header.
            global_header_node,
            # This is the content of the block.
            BlockNode(
                classes=[],
                engine="default",
                content=[
                    # This is the block header.
                    block_header_node,
                    # # This is the block ToC.
                    TocNode(
                        nested_entries=[block_header_toc_item_node],
                        plain_entries=[block_header_node],
                        info=NodeInfo(context=generate_context(7, 0, 7, 5)),
                    ),
                ],
                info=NodeInfo(
                    context=generate_context(4, 0, 8, 4),
                    named_args={"isolate": "true"},
                ),
            ),
            # This is the global ToC
            TocNode(
                nested_entries=[global_header_toc_item_node],
                plain_entries=[global_header_node],
                info=NodeInfo(context=generate_context(10, 0, 10, 5)),
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

    compare_asdict_list(
        parser.nodes,
        [
            BlockNode(
                classes=[],
                engine="default",
                content=[
                    ParagraphNode(
                        content=[
                            ParagraphLineNode(
                                content=[
                                    TextNode(
                                        "The answer is 42.",
                                        info=NodeInfo(
                                            context=generate_context(5, 0, 5, 17)
                                        ),
                                    ),
                                ],
                                info=NodeInfo(context=generate_context(5, 0, 5, 23)),
                            )
                        ],
                        info=NodeInfo(context=generate_context(5, 0, 5, 23)),
                    ),
                ],
                info=NodeInfo(
                    context=generate_context(2, 0, 6, 4),
                    named_args={"isolate": "true"},
                ),
            )
        ],
    )
