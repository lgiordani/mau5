import pytest

from mau.lexers.document_lexer import DocumentLexer
from mau.nodes.block import BlockNode
from mau.nodes.inline import TextNode
from mau.nodes.node import NodeInfo
from mau.parsers.base_parser import MauParserException
from mau.parsers.document_parser import DocumentParser
from mau.test_helpers import (
    compare_nodes_sequence,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_parse_block_title_and_arguments():
    source = """
    . Just a title
    [arg1, *subtype1, #tag1, key1=value1]
    ----
    ----
    """

    parser = runner(source)

    compare_nodes_sequence(
        parser.nodes,
        [
            BlockNode(
                classes=[],
                labels={
                    "title": [
                        TextNode(
                            "Just a title",
                            info=NodeInfo(context=generate_context(1, 2, 1, 14)),
                        )
                    ]
                },
                info=NodeInfo(
                    context=generate_context(3, 0, 4, 4),
                    unnamed_args=["arg1"],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
            ),
        ],
    )


def test_block_classes_single_class():
    source = """
    [*subtype1,classes=cls1]
    ----
    ----
    """

    parser = runner(source)

    compare_nodes_sequence(
        parser.nodes,
        [
            BlockNode(
                classes=["cls1"],
                info=NodeInfo(
                    context=generate_context(2, 0, 3, 4),
                    subtype="subtype1",
                ),
            )
        ],
    )


def test_block_classes_multiple_classes():
    source = """
    [*subtype1,classes="cls1,cls2"]
    ----
    ----
    """

    parser = runner(source)

    compare_nodes_sequence(
        parser.nodes,
        [
            BlockNode(
                classes=["cls1", "cls2"],
                info=NodeInfo(
                    context=generate_context(2, 0, 3, 4),
                    subtype="subtype1",
                ),
            )
        ],
    )


def test_block_engine():
    source = """
    [*subtype,engine=doesnotexist]
    ----
    ----
    """

    with pytest.raises(MauParserException) as exc:
        runner(source)

    assert exc.value.context == generate_context(2, 0, 3, 4)
