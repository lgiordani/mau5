from unittest.mock import patch

from mau.environment.environment import Environment
from mau.lexers.document_lexer import DocumentLexer
from mau.nodes.block import BlockSectionNodeContent
from mau.nodes.command import FootnotesItemNodeContent, FootnotesNodeContent
from mau.nodes.inline import TextNodeContent
from mau.nodes.lists import ListItemNodeContent, ListNodeContent
from mau.nodes.macros import MacroFootnoteNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.nodes.paragraph import ParagraphNodeContent, ParagraphLineNodeContent
from mau.parsers.document_parser import DocumentParser
from mau.test_helpers import (
    compare_node,
    compare_nodes,
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

    footnote_node = Node(
        content=FootnotesItemNodeContent("somename", "1", "XXYY"),
        info=NodeInfo(
            context=generate_context(4, 0, 6, 4),
            named_args={"footnote": "somename"},
        ),
        children={
            "content": [],
            "sections": [
                Node(
                    content=BlockSectionNodeContent("content"),
                    info=NodeInfo(context=generate_context(5, 0, 5, 10)),
                    children={
                        "content": [
                            Node(
                                content=ParagraphNodeContent(),
                                info=NodeInfo(context=generate_context(5, 0, 5, 10)),
                                children={
                                    "content": [
                                        Node(
                                            content=ParagraphLineNodeContent(),
                                            info=NodeInfo(
                                                context=generate_context(5, 0, 5, 10)
                                            ),
                                            children={
                                                "content": [
                                                    Node(
                                                        content=TextNodeContent(
                                                            "Some text."
                                                        ),
                                                        info=NodeInfo(
                                                            context=generate_context(
                                                                5, 0, 5, 10
                                                            )
                                                        ),
                                                    )
                                                ]
                                            },
                                        )
                                    ]
                                },
                            )
                        ],
                    },
                )
            ],
        },
    )

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(1, 0, 1, 45)),
                children={
                    "content": [
                        Node(
                            content=ParagraphLineNodeContent(),
                            info=NodeInfo(context=generate_context(1, 0, 1, 45)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent(
                                            "This contains a footnote"
                                        ),
                                        info=NodeInfo(
                                            context=generate_context(1, 0, 1, 24)
                                        ),
                                    ),
                                    Node(
                                        content=MacroFootnoteNodeContent(
                                            "somename", "1", "XXYY"
                                        ),
                                        info=NodeInfo(
                                            context=generate_context(1, 24, 1, 44)
                                        ),
                                        children={"footnote": [footnote_node]},
                                    ),
                                    Node(
                                        content=TextNodeContent("."),
                                        info=NodeInfo(
                                            context=generate_context(1, 44, 1, 45)
                                        ),
                                    ),
                                ]
                            },
                        )
                    ]
                },
            )
        ],
    )

    assert list(parser.footnotes_manager.data.keys()) == ["somename"]

    compare_node(parser.footnotes_manager.data["somename"], footnote_node)


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

    footnote_node = Node(
        content=FootnotesItemNodeContent("somename", "1", "XXYY"),
        info=NodeInfo(
            context=generate_context(4, 0, 6, 4),
            named_args={"footnote": "somename"},
        ),
        children={
            "content": [],
            "sections": [
                Node(
                    content=BlockSectionNodeContent("content"),
                    info=NodeInfo(context=generate_context(5, 0, 5, 10)),
                    children={
                        "content": [
                            Node(
                                content=ParagraphNodeContent(),
                                info=NodeInfo(context=generate_context(5, 0, 5, 10)),
                                children={
                                    "content": [
                                        Node(
                                            content=ParagraphLineNodeContent(),
                                            info=NodeInfo(
                                                context=generate_context(5, 0, 5, 10)
                                            ),
                                            children={
                                                "content": [
                                                    Node(
                                                        content=TextNodeContent(
                                                            "Some text."
                                                        ),
                                                        info=NodeInfo(
                                                            context=generate_context(
                                                                5, 0, 5, 10
                                                            )
                                                        ),
                                                    )
                                                ]
                                            },
                                        )
                                    ]
                                },
                            )
                        ],
                    },
                )
            ],
        },
    )

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=ListNodeContent(ordered=False, main_node=True),
                info=NodeInfo(context=generate_context(1, 0, 1, 47)),
                children={
                    "nodes": [
                        Node(
                            content=ListItemNodeContent("1"),
                            info=NodeInfo(context=generate_context(1, 0, 1, 47)),
                            children={
                                "text": [
                                    Node(
                                        content=TextNodeContent(
                                            "This contains a footnote"
                                        ),
                                        info=NodeInfo(
                                            context=generate_context(1, 2, 1, 26)
                                        ),
                                    ),
                                    Node(
                                        content=MacroFootnoteNodeContent(
                                            "somename", "1", "XXYY"
                                        ),
                                        info=NodeInfo(
                                            context=generate_context(1, 26, 1, 46)
                                        ),
                                        children={"footnote": [footnote_node]},
                                    ),
                                    Node(
                                        content=TextNodeContent("."),
                                        info=NodeInfo(
                                            context=generate_context(1, 46, 1, 47)
                                        ),
                                    ),
                                ]
                            },
                        )
                    ]
                },
            )
        ],
    )

    assert list(parser.footnotes_manager.data.keys()) == ["somename"]

    compare_node(parser.footnotes_manager.data["somename"], footnote_node)


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

    footnote_node = Node(
        content=FootnotesItemNodeContent("somename", "1", "XXYY"),
        info=NodeInfo(
            context=generate_context(4, 0, 6, 4),
            named_args={"footnote": "somename"},
        ),
        children={
            "content": [],
            "sections": [
                Node(
                    content=BlockSectionNodeContent("content"),
                    info=NodeInfo(context=generate_context(5, 0, 5, 10)),
                    children={
                        "content": [
                            Node(
                                content=ParagraphNodeContent(),
                                info=NodeInfo(context=generate_context(5, 0, 5, 10)),
                                children={
                                    "content": [
                                        Node(
                                            content=ParagraphLineNodeContent(),
                                            info=NodeInfo(
                                                context=generate_context(5, 0, 5, 10)
                                            ),
                                            children={
                                                "content": [
                                                    Node(
                                                        content=TextNodeContent(
                                                            "Some text."
                                                        ),
                                                        info=NodeInfo(
                                                            context=generate_context(
                                                                5, 0, 5, 10
                                                            )
                                                        ),
                                                    )
                                                ]
                                            },
                                        )
                                    ]
                                },
                            )
                        ],
                    },
                )
            ],
        },
    )

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(1, 0, 1, 45)),
                children={
                    "content": [
                        Node(
                            content=ParagraphLineNodeContent(),
                            info=NodeInfo(context=generate_context(1, 0, 1, 45)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent(
                                            "This contains a footnote"
                                        ),
                                        info=NodeInfo(
                                            context=generate_context(1, 0, 1, 24)
                                        ),
                                    ),
                                    Node(
                                        content=MacroFootnoteNodeContent(
                                            "somename", "1", "XXYY"
                                        ),
                                        info=NodeInfo(
                                            context=generate_context(1, 24, 1, 44)
                                        ),
                                        children={"footnote": [footnote_node]},
                                    ),
                                    Node(
                                        content=TextNodeContent("."),
                                        info=NodeInfo(
                                            context=generate_context(1, 44, 1, 45)
                                        ),
                                    ),
                                ]
                            },
                        ),
                    ]
                },
            ),
            Node(
                content=FootnotesNodeContent(),
                info=NodeInfo(context=generate_context(8, 0, 8, 11)),
                children={"entries": [footnote_node]},
            ),
        ],
    )

    assert list(parser.footnotes_manager.data.keys()) == ["somename"]

    compare_node(parser.footnotes_manager.data["somename"], footnote_node)


def test_command_footnotes_supports_boxed_arguments():
    source = """
    [arg1, *subtype1, #tag1, key1=value1]
    ::footnotes
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=FootnotesNodeContent(),
                info=NodeInfo(
                    context=generate_context(2, 0, 2, 11),
                    named_args={"key1": "value1"},
                    unnamed_args=["arg1"],
                    subtype="subtype1",
                    tags=["tag1"],
                ),
                children={"entries": []},
            ),
        ],
    )

    assert list(parser.footnotes_manager.data.keys()) == []


def test_command_footnotes_supports_inline_arguments():
    source = """
    ::footnotes:arg1, *subtype1, #tag1, key1=value1
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=FootnotesNodeContent(),
                info=NodeInfo(
                    context=generate_context(1, 0, 1, 11),
                    named_args={"key1": "value1"},
                    unnamed_args=["arg1"],
                    subtype="subtype1",
                    tags=["tag1"],
                ),
                children={"entries": []},
            ),
        ],
    )

    assert list(parser.footnotes_manager.data.keys()) == []


def test_command_footnotes_supports_labels():
    source = """
    . Some label
    ::footnotes
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=FootnotesNodeContent(),
                info=NodeInfo(context=generate_context(2, 0, 2, 11)),
                children={
                    "entries": [],
                    "title": [
                        Node(
                            content=TextNodeContent("Some label"),
                            info=NodeInfo(context=generate_context(1, 2, 1, 12)),
                        )
                    ],
                },
            ),
        ],
    )

    assert list(parser.footnotes_manager.data.keys()) == []


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

    compare_nodes(parser.nodes, [])

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

    footnote_node = Node(
        content=FootnotesItemNodeContent("somename", "1", "XXYY"),
        info=NodeInfo(
            context=generate_context(4, 0, 6, 4),
            subtype="footnote",
            named_args={"footnote": "somename"},
        ),
        children={
            "content": [],
            "sections": [
                Node(
                    content=BlockSectionNodeContent("content"),
                    info=NodeInfo(context=generate_context(5, 0, 5, 10)),
                    children={
                        "content": [
                            Node(
                                content=ParagraphNodeContent(),
                                info=NodeInfo(context=generate_context(5, 0, 5, 10)),
                                children={
                                    "content": [
                                        Node(
                                            content=ParagraphLineNodeContent(),
                                            info=NodeInfo(
                                                context=generate_context(5, 0, 5, 10)
                                            ),
                                            children={
                                                "content": [
                                                    Node(
                                                        content=TextNodeContent(
                                                            "Some text."
                                                        ),
                                                        info=NodeInfo(
                                                            context=generate_context(
                                                                5, 0, 5, 10
                                                            )
                                                        ),
                                                    )
                                                ]
                                            },
                                        )
                                    ]
                                },
                            )
                        ],
                    },
                )
            ],
        },
    )

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(1, 0, 1, 45)),
                children={
                    "content": [
                        Node(
                            content=ParagraphLineNodeContent(),
                            info=NodeInfo(context=generate_context(1, 0, 1, 45)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent(
                                            "This contains a footnote"
                                        ),
                                        info=NodeInfo(
                                            context=generate_context(1, 0, 1, 24)
                                        ),
                                    ),
                                    Node(
                                        content=MacroFootnoteNodeContent(
                                            "somename", "1", "XXYY"
                                        ),
                                        info=NodeInfo(
                                            context=generate_context(1, 24, 1, 44)
                                        ),
                                        children={"footnote": [footnote_node]},
                                    ),
                                    Node(
                                        content=TextNodeContent("."),
                                        info=NodeInfo(
                                            context=generate_context(1, 44, 1, 45)
                                        ),
                                    ),
                                ]
                            },
                        )
                    ]
                },
            )
        ],
    )

    assert list(parser.footnotes_manager.data.keys()) == ["somename"]

    compare_node(parser.footnotes_manager.data["somename"], footnote_node)
