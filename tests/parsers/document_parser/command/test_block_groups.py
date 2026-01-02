import pytest

from mau.environment.environment import Environment
from mau.lexers.document_lexer import DocumentLexer
from mau.nodes.block import BlockNodeContent, BlockSectionNodeContent
from mau.nodes.command import BlockGroupNodeContent
from mau.nodes.inline import TextNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.nodes.paragraph import ParagraphNodeContent, ParagraphLineNodeContent
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


def test_group_engine():
    source = """
    [group=group1, position=position1]
    ----
    Some text 1.
    ----

    [group=group1, position=position2]
    ----
    Some text 2.
    ----

    ::blockgroup:group1
    """

    parser = runner(source)

    block_node1 = Node(
        content=BlockNodeContent(engine="default"),
        info=NodeInfo(context=generate_context(2, 0, 4, 4)),
        children={
            "content": [],
            "sections": [
                Node(
                    content=BlockSectionNodeContent("content"),
                    info=NodeInfo(context=generate_context(3, 0, 3, 12)),
                    children={
                        "content": [
                            Node(
                                content=ParagraphNodeContent(),
                                info=NodeInfo(context=generate_context(3, 0, 3, 12)),
                                children={
                                    "content": [
                                        Node(
                                            content=ParagraphLineNodeContent(),
                                            info=NodeInfo(
                                                context=generate_context(3, 0, 3, 12)
                                            ),
                                            children={
                                                "content": [
                                                    Node(
                                                        content=TextNodeContent(
                                                            "Some text 1."
                                                        ),
                                                        info=NodeInfo(
                                                            context=generate_context(
                                                                3, 0, 3, 12
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

    block_node2 = Node(
        content=BlockNodeContent(engine="default"),
        info=NodeInfo(context=generate_context(7, 0, 9, 4)),
        children={
            "content": [],
            "sections": [
                Node(
                    content=BlockSectionNodeContent("content"),
                    info=NodeInfo(context=generate_context(8, 0, 8, 12)),
                    children={
                        "content": [
                            Node(
                                content=ParagraphNodeContent(),
                                info=NodeInfo(context=generate_context(8, 0, 8, 12)),
                                children={
                                    "content": [
                                        Node(
                                            content=ParagraphLineNodeContent(),
                                            info=NodeInfo(
                                                context=generate_context(8, 0, 8, 12)
                                            ),
                                            children={
                                                "content": [
                                                    Node(
                                                        content=TextNodeContent(
                                                            "Some text 2."
                                                        ),
                                                        info=NodeInfo(
                                                            context=generate_context(
                                                                8, 0, 8, 12
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
                content=BlockGroupNodeContent("group1"),
                info=NodeInfo(
                    context=generate_context(11, 0, 11, 12), unnamed_args=["group1"]
                ),
                children={"position1": [block_node1], "position2": [block_node2]},
            )
        ],
    )


def test_group_engine_wrong_group():
    source = """
    [group=group1, position=position1]
    ----
    Some text 1.
    ----

    [group=group1, position=position2]
    ----
    Some text 2.
    ----

    ::blockgroup:group2
    """

    with pytest.raises(MauParserException) as exc:
        runner(source)

    assert exc.value.context == generate_context(11, 0, 11, 12)


def test_command_toc_supports_inline_arguments():
    source = """
    [group=group1, position=position1]
    ----
    Some text 1.
    ----

    ::blockgroup:group1,arg1,#tag1,*subtype1,key1=value1
    """

    parser = runner(source)

    block_node1 = Node(
        content=BlockNodeContent(engine="default"),
        info=NodeInfo(context=generate_context(2, 0, 4, 4)),
        children={
            "content": [],
            "sections": [
                Node(
                    content=BlockSectionNodeContent("content"),
                    info=NodeInfo(context=generate_context(3, 0, 3, 12)),
                    children={
                        "content": [
                            Node(
                                content=ParagraphNodeContent(),
                                info=NodeInfo(context=generate_context(3, 0, 3, 12)),
                                children={
                                    "content": [
                                        Node(
                                            content=ParagraphLineNodeContent(),
                                            info=NodeInfo(
                                                context=generate_context(3, 0, 3, 12)
                                            ),
                                            children={
                                                "content": [
                                                    Node(
                                                        content=TextNodeContent(
                                                            "Some text 1."
                                                        ),
                                                        info=NodeInfo(
                                                            context=generate_context(
                                                                3, 0, 3, 12
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
                content=BlockGroupNodeContent("group1"),
                info=NodeInfo(
                    context=generate_context(6, 0, 6, 12),
                    unnamed_args=["group1", "arg1"],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
                children={
                    "position1": [block_node1],
                },
            )
        ],
    )


def test_command_toc_supports_boxed_arguments():
    source = """
    [group=group1, position=position1]
    ----
    Some text 1.
    ----

    [group1, arg1, #tag1, *subtype1, key1=value1]
    ::blockgroup
    """

    parser = runner(source)

    block_node1 = Node(
        content=BlockNodeContent(engine="default"),
        info=NodeInfo(context=generate_context(2, 0, 4, 4)),
        children={
            "content": [],
            "sections": [
                Node(
                    content=BlockSectionNodeContent("content"),
                    info=NodeInfo(context=generate_context(3, 0, 3, 12)),
                    children={
                        "content": [
                            Node(
                                content=ParagraphNodeContent(),
                                info=NodeInfo(context=generate_context(3, 0, 3, 12)),
                                children={
                                    "content": [
                                        Node(
                                            content=ParagraphLineNodeContent(),
                                            info=NodeInfo(
                                                context=generate_context(3, 0, 3, 12)
                                            ),
                                            children={
                                                "content": [
                                                    Node(
                                                        content=TextNodeContent(
                                                            "Some text 1."
                                                        ),
                                                        info=NodeInfo(
                                                            context=generate_context(
                                                                3, 0, 3, 12
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
                content=BlockGroupNodeContent("group1"),
                info=NodeInfo(
                    context=generate_context(7, 0, 7, 12),
                    unnamed_args=["group1", "arg1"],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
                children={
                    "position1": [block_node1],
                },
            )
        ],
    )


def test_command_toc_supports_labels():
    source = """
    [group=group1, position=position1]
    ----
    Some text 1.
    ----

    . Some label
    ::blockgroup:group1
    """

    parser = runner(source)

    block_node1 = Node(
        content=BlockNodeContent(engine="default"),
        info=NodeInfo(context=generate_context(2, 0, 4, 4)),
        children={
            "content": [],
            "sections": [
                Node(
                    content=BlockSectionNodeContent("content"),
                    info=NodeInfo(context=generate_context(3, 0, 3, 12)),
                    children={
                        "content": [
                            Node(
                                content=ParagraphNodeContent(),
                                info=NodeInfo(context=generate_context(3, 0, 3, 12)),
                                children={
                                    "content": [
                                        Node(
                                            content=ParagraphLineNodeContent(),
                                            info=NodeInfo(
                                                context=generate_context(3, 0, 3, 12)
                                            ),
                                            children={
                                                "content": [
                                                    Node(
                                                        content=TextNodeContent(
                                                            "Some text 1."
                                                        ),
                                                        info=NodeInfo(
                                                            context=generate_context(
                                                                3, 0, 3, 12
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
                content=BlockGroupNodeContent("group1"),
                info=NodeInfo(
                    context=generate_context(7, 0, 7, 12),
                    unnamed_args=["group1"],
                ),
                children={
                    "position1": [block_node1],
                    "title": [
                        Node(
                            content=TextNodeContent("Some label"),
                            info=NodeInfo(context=generate_context(6, 2, 6, 12)),
                        )
                    ],
                },
            )
        ],
    )


def test_command_toc_supports_control():
    environment = Environment()
    environment["answer"] = "24"

    source = """
    [group=group1, position=position1]
    ----
    Some text 1.
    ----

    @if answer==42
    [group1, arg1, arg2]
    . Some title
    ::blockgroup
    """

    parser = runner(source, environment)

    compare_nodes(parser.nodes, [])

    assert parser.arguments_buffer.arguments is None
    assert parser.label_buffer.labels == {}
    assert parser.control_buffer.control is None
