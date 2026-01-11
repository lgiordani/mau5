from unittest.mock import patch

from mau.environment.environment import Environment
from mau.lexers.document_lexer import DocumentLexer
from mau.nodes.block import BlockNodeData
from mau.nodes.footnotes import FootnoteNodeData
from mau.nodes.commands import FootnotesNodeData
from mau.nodes.inline import TextNodeData
from mau.nodes.lists import ListItemNodeData, ListNodeData
from mau.nodes.macros import MacroFootnoteNodeData
from mau.nodes.node import Node, NodeInfo
from mau.nodes.paragraph import ParagraphNodeData, ParagraphLineNodeData
from mau.parsers.document_parser import DocumentParser
from mau.test_helpers import (
    compare_asdict_object,
    compare_asdict_list,
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
        Node(
            data=ParagraphNodeData(
                content=[
                    Node(
                        data=ParagraphLineNodeData(
                            content=[
                                Node(
                                    data=TextNodeData("Some text."),
                                    info=NodeInfo(
                                        context=generate_context(5, 0, 5, 10)
                                    ),
                                )
                            ]
                        ),
                        info=NodeInfo(context=generate_context(5, 0, 5, 10)),
                    )
                ]
            ),
            info=NodeInfo(context=generate_context(5, 0, 5, 10)),
        )
    ]

    footnote_block_data = BlockNodeData(content=footnote_body_nodes, engine="default")

    footnote_data = FootnoteNodeData(
        name="somename",
        public_id="1",
        private_id="XXYY",
        content=footnote_body_nodes,
    )

    compare_asdict_list(
        parser.nodes,
        [
            Node(
                data=ParagraphNodeData(
                    content=[
                        Node(
                            data=ParagraphLineNodeData(
                                content=[
                                    Node(
                                        data=TextNodeData("This contains a footnote"),
                                        info=NodeInfo(
                                            context=generate_context(1, 0, 1, 24)
                                        ),
                                    ),
                                    Node(
                                        data=MacroFootnoteNodeData(
                                            footnote=footnote_data,
                                        ),
                                        info=NodeInfo(
                                            context=generate_context(1, 24, 1, 44)
                                        ),
                                    ),
                                    Node(
                                        data=TextNodeData("."),
                                        info=NodeInfo(
                                            context=generate_context(1, 44, 1, 45)
                                        ),
                                    ),
                                ]
                            ),
                            info=NodeInfo(context=generate_context(1, 0, 1, 45)),
                        )
                    ]
                ),
                info=NodeInfo(context=generate_context(1, 0, 1, 45)),
            )
        ],
    )

    compare_asdict_object(
        parser.footnotes_manager.bodies["somename"],
        footnote_block_data,
    )

    compare_asdict_list(
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
        Node(
            data=ParagraphNodeData(
                content=[
                    Node(
                        data=ParagraphLineNodeData(
                            content=[
                                Node(
                                    data=TextNodeData("Some text."),
                                    info=NodeInfo(
                                        context=generate_context(5, 0, 5, 10)
                                    ),
                                )
                            ]
                        ),
                        info=NodeInfo(context=generate_context(5, 0, 5, 10)),
                    )
                ]
            ),
            info=NodeInfo(context=generate_context(5, 0, 5, 10)),
        )
    ]

    footnote_block_data = BlockNodeData(content=footnote_body_nodes, engine="default")

    footnote_data = FootnoteNodeData(
        name="somename",
        public_id="1",
        private_id="XXYY",
        content=footnote_body_nodes,
    )

    compare_asdict_list(
        parser.nodes,
        [
            Node(
                data=ListNodeData(
                    ordered=False,
                    main_node=True,
                    content=[
                        Node(
                            data=ListItemNodeData(
                                1,
                                content=[
                                    Node(
                                        data=TextNodeData("This contains a footnote"),
                                        info=NodeInfo(
                                            context=generate_context(1, 2, 1, 26)
                                        ),
                                    ),
                                    Node(
                                        data=MacroFootnoteNodeData(
                                            footnote=footnote_data,
                                        ),
                                        info=NodeInfo(
                                            context=generate_context(1, 26, 1, 46)
                                        ),
                                    ),
                                    Node(
                                        data=TextNodeData("."),
                                        info=NodeInfo(
                                            context=generate_context(1, 46, 1, 47)
                                        ),
                                    ),
                                ],
                            ),
                            info=NodeInfo(context=generate_context(1, 0, 1, 47)),
                        )
                    ],
                ),
                info=NodeInfo(context=generate_context(1, 0, 1, 47)),
            )
        ],
    )

    compare_asdict_object(
        parser.footnotes_manager.bodies["somename"],
        footnote_block_data,
    )

    compare_asdict_list(
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
        Node(
            data=ParagraphNodeData(
                content=[
                    Node(
                        data=ParagraphLineNodeData(
                            content=[
                                Node(
                                    data=TextNodeData("Some text."),
                                    info=NodeInfo(
                                        context=generate_context(5, 0, 5, 10)
                                    ),
                                )
                            ]
                        ),
                        info=NodeInfo(context=generate_context(5, 0, 5, 10)),
                    )
                ]
            ),
            info=NodeInfo(context=generate_context(5, 0, 5, 10)),
        )
    ]

    footnote_block_data = BlockNodeData(content=footnote_body_nodes, engine="default")

    footnote_data = FootnoteNodeData(
        name="somename",
        public_id="1",
        private_id="XXYY",
        content=footnote_body_nodes,
    )

    compare_asdict_list(
        parser.nodes,
        [
            Node(
                data=ParagraphNodeData(
                    content=[
                        Node(
                            data=ParagraphLineNodeData(
                                content=[
                                    Node(
                                        data=TextNodeData("This contains a footnote"),
                                        info=NodeInfo(
                                            context=generate_context(1, 0, 1, 24)
                                        ),
                                    ),
                                    Node(
                                        data=MacroFootnoteNodeData(
                                            footnote=footnote_data,
                                        ),
                                        info=NodeInfo(
                                            context=generate_context(1, 24, 1, 44)
                                        ),
                                    ),
                                    Node(
                                        data=TextNodeData("."),
                                        info=NodeInfo(
                                            context=generate_context(1, 44, 1, 45)
                                        ),
                                    ),
                                ]
                            ),
                            info=NodeInfo(context=generate_context(1, 0, 1, 45)),
                        )
                    ]
                ),
                info=NodeInfo(context=generate_context(1, 0, 1, 45)),
            ),
            Node(
                data=FootnotesNodeData(footnotes=[footnote_data]),
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

    compare_asdict_list(
        parser.nodes,
        [
            Node(
                data=FootnotesNodeData(),
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

    compare_asdict_list(
        parser.nodes,
        [
            Node(
                data=FootnotesNodeData(),
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

    compare_asdict_list(
        parser.nodes,
        [
            Node(
                data=FootnotesNodeData(
                    labels={
                        "title": [
                            Node(
                                data=TextNodeData("Some label"),
                                info=NodeInfo(context=generate_context(1, 2, 1, 12)),
                            )
                        ]
                    }
                ),
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

    compare_asdict_list(parser.nodes, [])

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
        Node(
            data=ParagraphNodeData(
                content=[
                    Node(
                        data=ParagraphLineNodeData(
                            content=[
                                Node(
                                    data=TextNodeData("Some text."),
                                    info=NodeInfo(
                                        context=generate_context(5, 0, 5, 10)
                                    ),
                                )
                            ]
                        ),
                        info=NodeInfo(context=generate_context(5, 0, 5, 10)),
                    )
                ]
            ),
            info=NodeInfo(context=generate_context(5, 0, 5, 10)),
        )
    ]

    footnote_block_data = BlockNodeData(content=footnote_body_nodes, engine="default")

    footnote_data = FootnoteNodeData(
        name="somename",
        public_id="1",
        private_id="XXYY",
        content=footnote_body_nodes,
    )

    compare_asdict_list(
        parser.nodes,
        [
            Node(
                data=ParagraphNodeData(
                    content=[
                        Node(
                            data=ParagraphLineNodeData(
                                content=[
                                    Node(
                                        data=TextNodeData("This contains a footnote"),
                                        info=NodeInfo(
                                            context=generate_context(1, 0, 1, 24)
                                        ),
                                    ),
                                    Node(
                                        data=MacroFootnoteNodeData(
                                            footnote=footnote_data,
                                        ),
                                        info=NodeInfo(
                                            context=generate_context(1, 24, 1, 44)
                                        ),
                                    ),
                                    Node(
                                        data=TextNodeData("."),
                                        info=NodeInfo(
                                            context=generate_context(1, 44, 1, 45)
                                        ),
                                    ),
                                ]
                            ),
                            info=NodeInfo(context=generate_context(1, 0, 1, 45)),
                        )
                    ]
                ),
                info=NodeInfo(context=generate_context(1, 0, 1, 45)),
            )
        ],
    )

    compare_asdict_object(
        parser.footnotes_manager.bodies["somename"],
        footnote_block_data,
    )

    compare_asdict_list(
        parser.footnotes_manager.footnotes,
        [footnote_data],
    )
