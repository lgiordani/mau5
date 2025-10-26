import pytest

from mau.nodes.block import BlockNodeContent
from mau.nodes.command import BlockGroupNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.base_parser import MauParserException
from mau.parsers.managers.block_group_manager import (
    BlockGroupManager,
)
from mau.test_helpers import (
    compare_node,
    generate_context,
)


def test_block_group_manager():
    bgm = BlockGroupManager()

    block_node1 = Node(
        content=BlockNodeContent(),
        info=NodeInfo(generate_context(1, 2, 1, 2)),
    )

    block_node2 = Node(
        content=BlockNodeContent(),
        info=NodeInfo(generate_context(3, 4, 3, 4)),
    )

    block_node3 = Node(
        content=BlockNodeContent(),
        info=NodeInfo(generate_context(5, 6, 5, 6)),
    )

    bgm.add_block("group1", "position1", block_node1)
    bgm.add_block("group1", "position2", block_node2)
    bgm.add_block("group2", "position1", block_node3)

    assert bgm.groups == {
        "group1": {
            "position1": block_node1,
            "position2": block_node2,
        },
        "group2": {
            "position1": block_node3,
        },
    }


def test_block_group_manager_same_position():
    bgm = BlockGroupManager()

    block_node1 = Node(
        content=BlockNodeContent(),
        info=NodeInfo(generate_context(1, 2, 1, 2)),
    )

    block_node2 = Node(
        content=BlockNodeContent(),
        info=NodeInfo(generate_context(3, 4, 3, 4)),
    )

    bgm.add_block("group1", "position1", block_node1)

    with pytest.raises(MauParserException) as exc:
        bgm.add_block("group1", "position1", block_node2)

    assert exc.value.context == generate_context(3, 4, 3, 4)


def test_block_group_manager_add_group_node():
    bgm = BlockGroupManager()

    group_node = Node(
        content=BlockGroupNodeContent("somename"),
        info=NodeInfo(generate_context(1, 2, 1, 2)),
    )

    bgm.add_group_node(group_node)

    assert bgm.group_nodes == [group_node]


def test_block_group_manager_process():
    bgm = BlockGroupManager()

    block_node1 = Node(
        content=BlockNodeContent(),
        info=NodeInfo(generate_context(1, 2, 1, 2)),
    )

    block_node2 = Node(
        content=BlockNodeContent(),
        info=NodeInfo(generate_context(3, 4, 3, 4)),
    )

    block_node3 = Node(
        content=BlockNodeContent(),
        info=NodeInfo(generate_context(5, 6, 5, 6)),
    )

    bgm.add_block("group1", "position1", block_node1)
    bgm.add_block("group1", "position2", block_node2)
    bgm.add_block("group2", "position1", block_node3)

    group_node = Node(
        content=BlockGroupNodeContent("group1"),
        info=NodeInfo(context=generate_context(4, 2, 4, 2)),
    )

    bgm.add_group_node(group_node)

    expected_node = Node(
        content=BlockGroupNodeContent("group1"),
        info=NodeInfo(context=generate_context(4, 2, 4, 2)),
        children={"position1": [block_node1], "position2": [block_node2]},
    )

    bgm.process()

    compare_node(group_node, expected_node)


def test_block_group_manager_process_group_does_not_exist():
    bgm = BlockGroupManager()

    group_node = Node(
        content=BlockGroupNodeContent("group1"),
        info=NodeInfo(context=generate_context(4, 2, 4, 2)),
    )
    bgm.add_group_node(group_node)

    with pytest.raises(MauParserException) as exc:
        bgm.process()

    assert exc.value.message == "The group named group1 does not exist."
    assert exc.value.context == generate_context(4, 2, 4, 2)
