
import pytest

from mau.lexers.document_lexer.lexer import DocumentLexer
from mau.nodes.block import BlockNodeContent
from mau.nodes.inline import TextNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.nodes.paragraph import ParagraphNodeContent
from mau.parsers.base_parser.parser import MauParserException
from mau.parsers.document_parser.parser import DocumentParser
from mau.test_helpers import (
    compare_node,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_group_engine():
    source = """
    [group1, position1, engine=group]
    ----
    Some text 1.
    ----

    [group2, position2, engine=group]
    ----
    Some text 2.
    ----
    """

    parser = runner(source)

    compare_node(
        parser.block_group_manager.groups["group1"]["position1"],
        Node(
            content=BlockNodeContent(engine="group"),
            info=NodeInfo(context=generate_context(2, 0)),
            children={
                "content": [
                    Node(
                        content=ParagraphNodeContent(),
                        info=NodeInfo(context=generate_context(3, 0)),
                        children={
                            "content": [
                                Node(
                                    content=TextNodeContent("Some text 1."),
                                    info=NodeInfo(context=generate_context(3, 0)),
                                )
                            ]
                        },
                    )
                ],
            },
        ),
    )

    compare_node(
        parser.block_group_manager.groups["group2"]["position2"],
        Node(
            content=BlockNodeContent(engine="group"),
            info=NodeInfo(context=generate_context(7, 0)),
            children={
                "content": [
                    Node(
                        content=ParagraphNodeContent(),
                        info=NodeInfo(context=generate_context(8, 0)),
                        children={
                            "content": [
                                Node(
                                    content=TextNodeContent("Some text 2."),
                                    info=NodeInfo(context=generate_context(8, 0)),
                                )
                            ]
                        },
                    )
                ],
            },
        ),
    )


def test_group_engine_same_group_and_position():
    source = """
    [group1, position1, engine=group]
    ----
    Some text 1.
    ----

    [group1, position1, engine=group]
    ----
    Some text 2.
    ----
    """

    with pytest.raises(MauParserException) as exc:
        runner(source)

    assert (
        exc.value.message
        == f"Position position1 is already taken in group group1 by the block at {generate_context(2, 0)}"
    )
    assert exc.value.context == generate_context(7, 0)
