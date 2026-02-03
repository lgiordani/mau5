import pytest

from mau.environment.environment import Environment
from mau.lexers.document_lexer import DocumentLexer
from mau.nodes.block import BlockNode
from mau.nodes.command import BlockGroupNode
from mau.nodes.inline import TextNode
from mau.nodes.node import NodeInfo
from mau.nodes.node_arguments import NodeArguments
from mau.nodes.paragraph import ParagraphLineNode, ParagraphNode
from mau.parsers.document_parser import DocumentParser
from mau.test_helpers import (
    check_parent,
    compare_nodes_sequence,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_group():
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

    block_node1 = BlockNode(
        content=[
            ParagraphNode(
                lines=[
                    ParagraphLineNode(
                        content=[
                            TextNode(
                                "Some text 1.",
                                info=NodeInfo(context=generate_context(3, 0, 3, 12)),
                            )
                        ],
                        info=NodeInfo(context=generate_context(3, 0, 3, 12)),
                    )
                ],
                info=NodeInfo(context=generate_context(3, 0, 3, 12)),
            )
        ],
        arguments=NodeArguments(
            named_args={"group": "group1", "position": "position1"},
        ),
        info=NodeInfo(
            context=generate_context(2, 0, 4, 4),
        ),
    )

    block_node2 = BlockNode(
        content=[
            ParagraphNode(
                lines=[
                    ParagraphLineNode(
                        content=[
                            TextNode(
                                "Some text 2.",
                                info=NodeInfo(context=generate_context(8, 0, 8, 12)),
                            )
                        ],
                        info=NodeInfo(context=generate_context(8, 0, 8, 12)),
                    )
                ],
                info=NodeInfo(context=generate_context(8, 0, 8, 12)),
            )
        ],
        arguments=NodeArguments(
            named_args={"group": "group1", "position": "position2"},
        ),
        info=NodeInfo(
            context=generate_context(7, 0, 9, 4),
        ),
    )

    compare_nodes_sequence(
        parser.nodes,
        [
            BlockGroupNode(
                "group1",
                blocks={"position1": block_node1, "position2": block_node2},
                info=NodeInfo(
                    context=generate_context(11, 0, 11, 12),
                ),
            )
        ],
    )


def test_group_wrong_group():
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

    with pytest.raises(ValueError):
        runner(source)


def test_command_toc_supports_inline_arguments():
    source = """
    [group=group1, position=position1]
    ----
    Some text 1.
    ----

    ::blockgroup:group1,arg1,#tag1,*subtype1,key1=value1
    """

    parser = runner(source)

    block_node1 = BlockNode(
        content=[
            ParagraphNode(
                lines=[
                    ParagraphLineNode(
                        content=[
                            TextNode(
                                "Some text 1.",
                                info=NodeInfo(context=generate_context(3, 0, 3, 12)),
                            )
                        ],
                        info=NodeInfo(context=generate_context(3, 0, 3, 12)),
                    )
                ],
                info=NodeInfo(context=generate_context(3, 0, 3, 12)),
            )
        ],
        arguments=NodeArguments(
            named_args={"group": "group1", "position": "position1"},
        ),
        info=NodeInfo(
            context=generate_context(2, 0, 4, 4),
        ),
    )

    compare_nodes_sequence(
        parser.nodes,
        [
            BlockGroupNode(
                "group1",
                blocks={"position1": block_node1},
                arguments=NodeArguments(
                    unnamed_args=["arg1"],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
                info=NodeInfo(
                    context=generate_context(6, 0, 6, 12),
                ),
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

    block_node1 = BlockNode(
        content=[
            ParagraphNode(
                lines=[
                    ParagraphLineNode(
                        content=[
                            TextNode(
                                "Some text 1.",
                                info=NodeInfo(context=generate_context(3, 0, 3, 12)),
                            )
                        ],
                        info=NodeInfo(context=generate_context(3, 0, 3, 12)),
                    )
                ],
                info=NodeInfo(context=generate_context(3, 0, 3, 12)),
            )
        ],
        arguments=NodeArguments(
            named_args={"group": "group1", "position": "position1"},
        ),
        info=NodeInfo(
            context=generate_context(2, 0, 4, 4),
        ),
    )

    compare_nodes_sequence(
        parser.nodes,
        [
            BlockGroupNode(
                "group1",
                blocks={"position1": block_node1},
                arguments=NodeArguments(
                    unnamed_args=["arg1"],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
                info=NodeInfo(
                    context=generate_context(7, 0, 7, 12),
                ),
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

    block_node1 = BlockNode(
        content=[
            ParagraphNode(
                lines=[
                    ParagraphLineNode(
                        content=[
                            TextNode(
                                "Some text 1.",
                                info=NodeInfo(context=generate_context(3, 0, 3, 12)),
                            )
                        ],
                        info=NodeInfo(context=generate_context(3, 0, 3, 12)),
                    )
                ],
                info=NodeInfo(context=generate_context(3, 0, 3, 12)),
            )
        ],
        arguments=NodeArguments(
            named_args={"group": "group1", "position": "position1"},
        ),
        info=NodeInfo(
            context=generate_context(2, 0, 4, 4),
        ),
    )

    compare_nodes_sequence(
        parser.nodes,
        [
            BlockGroupNode(
                "group1",
                blocks={"position1": block_node1},
                labels={
                    "title": [
                        TextNode(
                            "Some label",
                            info=NodeInfo(context=generate_context(6, 2, 6, 12)),
                        )
                    ]
                },
                info=NodeInfo(
                    context=generate_context(7, 0, 7, 12),
                ),
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

    compare_nodes_sequence(parser.nodes, [])

    assert parser.arguments_buffer.arguments is None
    assert parser.label_buffer.labels == {}
    assert parser.control_buffer.control is None


def test_block_group_parenthood():
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

    document_node = parser.output.document

    block_group_node = parser.nodes[0]

    # All parser nodes must be
    # children of the document node.
    check_parent(document_node, parser.nodes)

    # All nodes inside the block group must be
    # children of the command.
    check_parent(block_group_node, block_group_node.blocks.values())


def test_block_group_parenthood_labels():
    source = """
    [group=group1, position=position1]
    ----
    Some text 1.
    ----

    [group=group1, position=position2]
    ----
    Some text 2.
    ----

    . A label
    .role Another label
    ::blockgroup:group1
    """

    parser = runner(source)

    block_group_node = parser.nodes[0]
    label_title_nodes = block_group_node.labels["title"]
    label_role_nodes = block_group_node.labels["role"]

    # Each label must be a child of the
    # block group it has been assigned to.
    check_parent(block_group_node, label_title_nodes)
    check_parent(block_group_node, label_role_nodes)
