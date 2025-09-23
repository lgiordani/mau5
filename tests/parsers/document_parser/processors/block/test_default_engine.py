from unittest.mock import patch

import pytest

from mau.lexers.document_lexer.lexer import DocumentLexer
from mau.nodes.block import BlockNodeContent
from mau.nodes.headers import HeaderNodeContent
from mau.nodes.inline import TextNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.base_parser.parser import MauParserException
from mau.parsers.document_parser.parser import DocumentParser
from mau.parsers.document_parser.processors.block import EngineType
from mau.test_helpers import (
    compare_nodes,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


@patch("mau.parsers.document_parser.managers.toc_manager.default_header_unique_id")
def test_default_engine_adds_headers_to_global_toc(mock_header_unique_id):
    mock_header_unique_id.return_value = "XXYY"

    source = """
    = Global header

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
                    engine=EngineType.DEFAULT.value,
                    preprocessor=None,
                ),
                info=NodeInfo(context=generate_context(3, 0)),
                children={
                    "content": [
                        Node(
                            content=HeaderNodeContent(1, "XXYY"),
                            info=NodeInfo(context=generate_context(4, 0)),
                            children={
                                "text": [
                                    Node(
                                        content=TextNodeContent("Block header"),
                                        info=NodeInfo(context=generate_context(4, 2)),
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
            Node(
                content=HeaderNodeContent(1, "XXYY"),
                info=NodeInfo(context=generate_context(4, 0)),
                children={
                    "text": [
                        Node(
                            content=TextNodeContent("Block header"),
                            info=NodeInfo(context=generate_context(4, 2)),
                        )
                    ],
                },
            ),
        ],
    )


def test_engine_not_available():
    source = """
    [engine=doesnotexist]
    ----
    = Block header
    ----
    """

    with pytest.raises(MauParserException) as exc:
        runner(source)

    assert exc.value.context == generate_context(2, 0)
