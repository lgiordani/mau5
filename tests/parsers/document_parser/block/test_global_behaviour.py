import pytest

from mau.nodes.paragraph import ParagraphNodeContent
from mau.lexers.document_lexer import DocumentLexer
from mau.nodes.block import BlockNodeContent
from mau.nodes.inline import TextNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.base_parser import MauParserException
from mau.parsers.document_parser import DocumentParser
from mau.token import Token, TokenType
from mau.text_buffer import Context
from mau.parsers.document_processors.block import (
    EngineType,
    parse_block_content_sections,
)
from mau.test_helpers import (
    dedent,
    compare_nodes,
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

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=BlockNodeContent(
                    classes=[],
                    engine=EngineType.DEFAULT.value,
                    preprocessor=None,
                ),
                info=NodeInfo(
                    context=generate_context(3, 0, 4, 4),
                    unnamed_args=["arg1"],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
                children={
                    "content": [],
                    "title": [
                        Node(
                            content=TextNodeContent("Just a title"),
                            info=NodeInfo(context=generate_context(1, 2, 1, 14)),
                        )
                    ],
                },
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

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=BlockNodeContent(
                    classes=["cls1"],
                    engine=EngineType.DEFAULT.value,
                    preprocessor=None,
                ),
                info=NodeInfo(
                    context=generate_context(2, 0, 3, 4),
                    subtype="subtype1",
                ),
                children={
                    "content": [],
                },
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

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=BlockNodeContent(
                    classes=["cls1", "cls2"],
                    engine=EngineType.DEFAULT.value,
                    preprocessor=None,
                ),
                info=NodeInfo(
                    context=generate_context(2, 0, 3, 4),
                    subtype="subtype1",
                ),
                children={
                    "content": [],
                },
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
