from unittest.mock import patch

from mau.environment.environment import Environment
from mau.lexers.document_lexer import DocumentLexer
from mau.nodes.block import BlockNode
from mau.nodes.commands import FootnotesNode
from mau.nodes.footnotes import FootnoteNode
from mau.nodes.inline import TextNode
from mau.nodes.lists import ListItemNode, ListNode
from mau.nodes.macros import MacroFootnoteNode
from mau.nodes.node import NodeInfo
from mau.nodes.paragraph import ParagraphLineNode, ParagraphNode
from mau.parsers.document_parser import DocumentParser
from mau.test_helpers import (
    compare_nodes,
    compare_nodes_sequence,
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

    [footnote=somename]
    ----
    Some text.
    ----
    """

    parser = runner(source)

    footnote_body_nodes = [
        ParagraphNode(
            lines=[
                ParagraphLineNode(
                    content=[
                        TextNode(
                            "Some text.",
                            info=NodeInfo(context=generate_context(5, 0, 5, 10)),
                        )
                    ],
                    info=NodeInfo(context=generate_context(5, 0, 5, 10)),
                )
            ],
            info=NodeInfo(context=generate_context(5, 0, 5, 10)),
        )
    ]

    footnote_block_data = BlockNode(content=footnote_body_nodes, engine="default")

    footnote_data = FootnoteNode(
        name="somename",
        public_id="1",
        private_id="XXYY",
        content=footnote_body_nodes,
    )

    compare_nodes_sequence(
        parser.nodes,
        [
            ParagraphNode(
                lines=[
                    ParagraphLineNode(
                        content=[
                            TextNode(
                                "This contains a footnote",
                                info=NodeInfo(context=generate_context(1, 0, 1, 24)),
                            ),
                            MacroFootnoteNode(
                                footnote=footnote_data,
                                info=NodeInfo(context=generate_context(1, 24, 1, 44)),
                            ),
                            TextNode(
                                ".",
                                info=NodeInfo(context=generate_context(1, 44, 1, 45)),
                            ),
                        ],
                        info=NodeInfo(context=generate_context(1, 0, 1, 45)),
                    )
                ],
                info=NodeInfo(context=generate_context(1, 0, 1, 45)),
            )
        ],
    )

    compare_nodes(
        parser.footnotes_manager.bodies["somename"],
        footnote_block_data,
    )

    compare_nodes_sequence(
        parser.footnotes_manager.footnotes,
        [footnote_data],
    )


@patch("mau.parsers.managers.footnotes_manager.default_footnote_unique_id")
def test_footnotes_in_lists_are_processed(mock_footnote_unique_id):
    mock_footnote_unique_id.return_value = "XXYY"

    source = """
    * This contains a footnote[footnote](somename).

    [footnote=somename]
    ----
    Some text.
    ----
    """

    parser = runner(source)

    footnote_body_nodes = [
        ParagraphNode(
            lines=[
                ParagraphLineNode(
                    content=[
                        TextNode(
                            "Some text.",
                            info=NodeInfo(context=generate_context(5, 0, 5, 10)),
                        )
                    ],
                    info=NodeInfo(context=generate_context(5, 0, 5, 10)),
                )
            ],
            info=NodeInfo(context=generate_context(5, 0, 5, 10)),
        )
    ]

    footnote_block_data = BlockNode(content=footnote_body_nodes, engine="default")

    footnote_data = FootnoteNode(
        name="somename",
        public_id="1",
        private_id="XXYY",
        content=footnote_body_nodes,
    )

    compare_nodes_sequence(
        parser.nodes,
        [
            ListNode(
                ordered=False,
                main_node=True,
                content=[
                    ListItemNode(
                        1,
                        content=[
                            TextNode(
                                "This contains a footnote",
                                info=NodeInfo(context=generate_context(1, 2, 1, 26)),
                            ),
                            MacroFootnoteNode(
                                footnote=footnote_data,
                                info=NodeInfo(context=generate_context(1, 26, 1, 46)),
                            ),
                            TextNode(
                                ".",
                                info=NodeInfo(context=generate_context(1, 46, 1, 47)),
                            ),
                        ],
                        info=NodeInfo(context=generate_context(1, 0, 1, 47)),
                    )
                ],
                info=NodeInfo(context=generate_context(1, 0, 1, 47)),
            )
        ],
    )

    compare_nodes(
        parser.footnotes_manager.bodies["somename"],
        footnote_block_data,
    )

    compare_nodes_sequence(
        parser.footnotes_manager.footnotes,
        [footnote_data],
    )


@patch("mau.parsers.managers.footnotes_manager.default_footnote_unique_id")
def test_command_footnotes(mock_footnote_unique_id):
    mock_footnote_unique_id.return_value = "XXYY"

    source = """
    This contains a footnote[footnote](somename).

    [footnote=somename]
    ----
    Some text.
    ----

    ::footnotes
    """

    parser = runner(source)

    footnote_body_nodes = [
        ParagraphNode(
            lines=[
                ParagraphLineNode(
                    content=[
                        TextNode(
                            "Some text.",
                            info=NodeInfo(context=generate_context(5, 0, 5, 10)),
                        )
                    ],
                    info=NodeInfo(context=generate_context(5, 0, 5, 10)),
                )
            ],
            info=NodeInfo(context=generate_context(5, 0, 5, 10)),
        )
    ]

    footnote_data = FootnoteNode(
        name="somename",
        public_id="1",
        private_id="XXYY",
        content=footnote_body_nodes,
    )

    compare_nodes_sequence(
        parser.nodes,
        [
            ParagraphNode(
                lines=[
                    ParagraphLineNode(
                        content=[
                            TextNode(
                                "This contains a footnote",
                                info=NodeInfo(context=generate_context(1, 0, 1, 24)),
                            ),
                            MacroFootnoteNode(
                                footnote=footnote_data,
                                info=NodeInfo(context=generate_context(1, 24, 1, 44)),
                            ),
                            TextNode(
                                ".",
                                info=NodeInfo(context=generate_context(1, 44, 1, 45)),
                            ),
                        ],
                        info=NodeInfo(context=generate_context(1, 0, 1, 45)),
                    )
                ],
                info=NodeInfo(context=generate_context(1, 0, 1, 45)),
            ),
            FootnotesNode(
                footnotes=[footnote_data],
                info=NodeInfo(context=generate_context(8, 0, 8, 11)),
            ),
        ],
    )


def test_command_footnotes_supports_boxed_arguments():
    source = """
    [arg1, *subtype1, #tag1, key1=value1]
    ::footnotes
    """

    parser = runner(source)

    compare_nodes_sequence(
        parser.nodes,
        [
            FootnotesNode(
                info=NodeInfo(
                    context=generate_context(2, 0, 2, 11),
                    named_args={"key1": "value1"},
                    unnamed_args=["arg1"],
                    subtype="subtype1",
                    tags=["tag1"],
                ),
            ),
        ],
    )


def test_command_footnotes_supports_inline_arguments():
    source = """
    ::footnotes:arg1, *subtype1, #tag1, key1=value1
    """

    parser = runner(source)

    compare_nodes_sequence(
        parser.nodes,
        [
            FootnotesNode(
                info=NodeInfo(
                    context=generate_context(1, 0, 1, 11),
                    named_args={"key1": "value1"},
                    unnamed_args=["arg1"],
                    subtype="subtype1",
                    tags=["tag1"],
                ),
            ),
        ],
    )


def test_command_footnotes_supports_labels():
    source = """
    . Some label
    ::footnotes
    """

    parser = runner(source)

    compare_nodes_sequence(
        parser.nodes,
        [
            FootnotesNode(
                labels={
                    "title": [
                        TextNode(
                            "Some label",
                            info=NodeInfo(context=generate_context(1, 2, 1, 12)),
                        )
                    ]
                },
                info=NodeInfo(context=generate_context(2, 0, 2, 11)),
            ),
        ],
    )


def test_command_footnotes_supports_control():
    environment = Environment()
    environment["answer"] = "24"

    source = """
    @if answer==42
    [arg1, arg2]
    . Some title
    ::footnotes
    """

    parser = runner(source, environment)

    compare_nodes_sequence(parser.nodes, [])

    assert parser.arguments_buffer.arguments is None
    assert parser.label_buffer.labels == {}
    assert parser.control_buffer.control is None


@patch("mau.parsers.managers.footnotes_manager.default_footnote_unique_id")
def test_footnotes_block_alias(mock_footnote_unique_id):
    mock_footnote_unique_id.return_value = "XXYY"

    source = """
    This contains a footnote[footnote](somename).

    [*footnote, somename]
    ----
    Some text.
    ----
    """

    parser = runner(source)

    footnote_body_nodes = [
        ParagraphNode(
            lines=[
                ParagraphLineNode(
                    content=[
                        TextNode(
                            "Some text.",
                            info=NodeInfo(context=generate_context(5, 0, 5, 10)),
                        )
                    ],
                    info=NodeInfo(context=generate_context(5, 0, 5, 10)),
                )
            ],
            info=NodeInfo(context=generate_context(5, 0, 5, 10)),
        )
    ]

    footnote_block_data = BlockNode(content=footnote_body_nodes, engine="default")

    footnote_data = FootnoteNode(
        name="somename",
        public_id="1",
        private_id="XXYY",
        content=footnote_body_nodes,
    )

    compare_nodes_sequence(
        parser.nodes,
        [
            ParagraphNode(
                lines=[
                    ParagraphLineNode(
                        content=[
                            TextNode(
                                "This contains a footnote",
                                info=NodeInfo(context=generate_context(1, 0, 1, 24)),
                            ),
                            MacroFootnoteNode(
                                footnote=footnote_data,
                                info=NodeInfo(context=generate_context(1, 24, 1, 44)),
                            ),
                            TextNode(
                                ".",
                                info=NodeInfo(context=generate_context(1, 44, 1, 45)),
                            ),
                        ],
                        info=NodeInfo(context=generate_context(1, 0, 1, 45)),
                    )
                ],
                info=NodeInfo(context=generate_context(1, 0, 1, 45)),
            )
        ],
    )

    compare_nodes(
        parser.footnotes_manager.bodies["somename"],
        footnote_block_data,
    )

    compare_nodes_sequence(
        parser.footnotes_manager.footnotes,
        [footnote_data],
    )
