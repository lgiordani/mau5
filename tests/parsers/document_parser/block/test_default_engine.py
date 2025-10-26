from unittest.mock import patch

import pytest

from mau.lexers.document_lexer import DocumentLexer
from mau.nodes.block import BlockNodeContent
from mau.nodes.headers import HeaderNodeContent
from mau.nodes.inline import TextNodeContent
from mau.nodes.macros import MacroFootnoteNodeContent
from mau.nodes.paragraph import ParagraphNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.base_parser import MauParserException
from mau.parsers.document_parser import DocumentParser
from mau.parsers.document_processors.block import EngineType
from mau.test_helpers import (
    compare_nodes,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


@patch("mau.parsers.managers.toc_manager.default_header_internal_id")
def test_default_engine_adds_headers_to_global_toc(mock_header_internal_id):
    mock_header_internal_id.return_value = "XXYY"

    source = """
    ----
    = Block header
    ----
    """

    parser = runner(source)

    assert len(parser.toc_manager.headers) == 1


def test_default_engine_adds_footnotes_to_global_toc():
    source = """
    ----
    Some text with a [footnote](note).

    [note, engine=footnote]
    ####
    Some text.
    ####
    ----
    """

    parser = runner(source)

    assert len(parser.footnotes_manager.mentions) == 1
    assert "note" in parser.footnotes_manager.data


def test_parse_block_disable_sections_on_text_without_sections():
    source = """
    [enable_sections=false]
    ----
    Some text.
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
                    context=generate_context(2, 0, 4, 4),
                    named_args={"enable_sections": "false"},
                ),
                children={
                    "content": [
                        Node(
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent("Some text."),
                                        info=NodeInfo(
                                            context=generate_context(3, 0, 3, 10)
                                        ),
                                    ),
                                ]
                            },
                            content=ParagraphNodeContent(),
                            info=NodeInfo(context=generate_context(3, 0, 3, 10)),
                        ),
                    ]
                },
            )
        ],
    )


def test_parse_block_disable_sections_on_text_with_sections():
    source = """
    [enable_sections=false]
    ----
    ++ Section 1
    Some text.
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
                    context=generate_context(2, 0, 5, 4),
                    named_args={"enable_sections": "false"},
                ),
                children={
                    "content": [
                        Node(
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent(
                                            "++ Section 1 Some text."
                                        ),
                                        info=NodeInfo(
                                            context=generate_context(3, 0, 3, 23)
                                        ),
                                    ),
                                ]
                            },
                            content=ParagraphNodeContent(),
                            info=NodeInfo(context=generate_context(3, 0, 4, 12)),
                        ),
                    ]
                },
            )
        ],
    )


def test_parse_block_enable_sections_on_text_without_sections():
    source = """
    [enable_sections=true]
    ----
    Some text.
    ----
    """

    with pytest.raises(MauParserException):
        runner(source)


def test_parse_block_enable_sections_on_text_with_sections():
    source = """
    [enable_sections=true]
    ----
    ++ Section 1
    Some text.
    ++ Section 2
    Some text 2a.
    Some text 2b.
    ++ Section 3
    ++ Section 4
    Some text 4.
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
                    context=generate_context(2, 0, 11, 4),
                    named_args={"enable_sections": "true"},
                ),
                children={
                    "content": [],
                    "Section 1": [
                        Node(
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent("Some text."),
                                        info=NodeInfo(
                                            context=generate_context(4, 0, 4, 10)
                                        ),
                                    ),
                                ]
                            },
                            content=ParagraphNodeContent(),
                            info=NodeInfo(context=generate_context(4, 0, 4, 10)),
                        ),
                    ],
                    "Section 2": [
                        Node(
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent(
                                            "Some text 2a. Some text 2b."
                                        ),
                                        info=NodeInfo(
                                            context=generate_context(6, 0, 6, 27)
                                        ),
                                    ),
                                ]
                            },
                            content=ParagraphNodeContent(),
                            info=NodeInfo(context=generate_context(6, 0, 7, 13)),
                        ),
                    ],
                    "Section 3": [],
                    "Section 4": [
                        Node(
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent("Some text 4."),
                                        info=NodeInfo(
                                            context=generate_context(10, 0, 10, 12)
                                        ),
                                    ),
                                ]
                            },
                            content=ParagraphNodeContent(),
                            info=NodeInfo(context=generate_context(10, 0, 10, 12)),
                        ),
                    ],
                },
            )
        ],
    )


def test_parse_block_sections_ignore_trailing_empty_lines():
    source = """
    [enable_sections=true]
    ----
    ++ Section 1
    Some text.

    
    ++ Section 2
    Some text 2.
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
                    context=generate_context(2, 0, 9, 4),
                    named_args={"enable_sections": "true"},
                ),
                children={
                    "content": [],
                    "Section 1": [
                        Node(
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent("Some text."),
                                        info=NodeInfo(
                                            context=generate_context(4, 0, 4, 10)
                                        ),
                                    ),
                                ]
                            },
                            content=ParagraphNodeContent(),
                            info=NodeInfo(context=generate_context(4, 0, 4, 10)),
                        ),
                    ],
                    "Section 2": [
                        Node(
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent("Some text 2."),
                                        info=NodeInfo(
                                            context=generate_context(8, 0, 8, 12)
                                        ),
                                    ),
                                ]
                            },
                            content=ParagraphNodeContent(),
                            info=NodeInfo(context=generate_context(8, 0, 8, 12)),
                        ),
                    ],
                },
            )
        ],
    )


def test_parse_block_sections_keep_empty_lines():
    source = """
    [enable_sections=true]
    ----
    ++ Section 1
    Some text 1a.

    Some text 1b.
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
                    context=generate_context(2, 0, 7, 4),
                    named_args={"enable_sections": "true"},
                ),
                children={
                    "content": [],
                    "Section 1": [
                        Node(
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent("Some text 1a."),
                                        info=NodeInfo(
                                            context=generate_context(4, 0, 4, 13)
                                        ),
                                    ),
                                ]
                            },
                            content=ParagraphNodeContent(),
                            info=NodeInfo(context=generate_context(4, 0, 4, 13)),
                        ),
                        Node(
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent("Some text 1b."),
                                        info=NodeInfo(
                                            context=generate_context(6, 0, 6, 13)
                                        ),
                                    ),
                                ]
                            },
                            content=ParagraphNodeContent(),
                            info=NodeInfo(context=generate_context(6, 0, 6, 13)),
                        ),
                    ],
                },
            )
        ],
    )
