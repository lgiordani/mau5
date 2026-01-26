from unittest.mock import patch

import pytest

from mau.nodes.block import BlockNode
from mau.nodes.command import FootnotesItemNode, FootnotesNode
from mau.nodes.footnote import FootnoteNode
from mau.parsers.managers.footnotes_manager import FootnotesManager
from mau.test_helpers import compare_nodes_sequence


def test_footnotes_manager_init():
    fnm = FootnotesManager()

    assert fnm.footnotes == []
    assert fnm.bodies == {}
    assert fnm.footnotes_list_nodes == []


def test_footnotes_manager_add_mention():
    fnm = FootnotesManager()

    footnote_node = FootnoteNode("name")

    fnm.add_footnote(footnote_node)

    assert fnm.footnotes == [footnote_node]
    assert fnm.bodies == {}
    assert fnm.footnotes_list_nodes == []


def test_footnotes_manager_add_mentions():
    fnm = FootnotesManager()

    footnote_node = FootnoteNode("name")

    fnm.add_footnotes([footnote_node])

    assert fnm.footnotes == [footnote_node]
    assert fnm.bodies == {}
    assert fnm.footnotes_list_nodes == []


def test_footnotes_manager_add_node():
    fnm = FootnotesManager()

    footnote_name = "name"
    footnote_block_node = BlockNode()
    footnote_body = footnote_block_node

    fnm.add_body(footnote_name, footnote_body)

    assert fnm.footnotes == []
    assert fnm.bodies == {footnote_name: footnote_block_node}
    assert fnm.footnotes_list_nodes == []


def test_footnotes_manager_add_node_duplicate_name():
    fnm = FootnotesManager()

    footnote_name = "name"

    footnote_block_node1 = BlockNode()
    footnote_body1 = footnote_block_node1

    footnote_block_node2 = BlockNode()
    footnote_body2 = footnote_block_node2

    fnm.add_body(footnote_name, footnote_body1)

    with pytest.raises(ValueError):
        fnm.add_body(footnote_name, footnote_body2)

    assert fnm.footnotes == []
    assert fnm.bodies == {footnote_name: footnote_block_node1}
    assert fnm.footnotes_list_nodes == []


def test_footnotes_manager_add_footnotes_list():
    fnm = FootnotesManager()

    footnote_list = FootnotesNode()

    fnm.add_footnotes_list(footnote_list)

    assert fnm.footnotes == []
    assert fnm.bodies == {}
    assert fnm.footnotes_list_nodes == [footnote_list]


def test_footnotes_manager_update():
    fnm = FootnotesManager()
    footnote_name = "name"

    footnote_node = FootnoteNode(footnote_name)
    fnm.add_footnote(footnote_node)

    footnote_block_node = BlockNode()
    footnote_body = footnote_block_node
    fnm.add_body(footnote_name, footnote_body)

    footnote_list = FootnotesNode()
    fnm.add_footnotes_list(footnote_list)

    other_fnm = FootnotesManager()
    other_fnm.update(fnm)

    assert other_fnm.footnotes == [footnote_node]
    assert other_fnm.bodies == {footnote_name: footnote_block_node}
    assert other_fnm.footnotes_list_nodes == [footnote_list]


@patch("mau.parsers.managers.footnotes_manager.default_footnote_unique_id")
def test_footnotes_manager_process(mock_footnote_unique_id):
    mock_footnote_unique_id.return_value = "XXYY"

    fnm = FootnotesManager()

    footnote_name1 = "footnote_name1"
    footnote_name2 = "footnote_name2"

    footnote_node1 = FootnoteNode(footnote_name1)
    fnm.add_footnote(footnote_node1)

    footnote_node2 = FootnoteNode(footnote_name2)
    fnm.add_footnote(footnote_node2)

    footnote_block_node1 = BlockNode()
    footnote_body1 = footnote_block_node1
    fnm.add_body(footnote_name1, footnote_body1)

    footnote_block_node2 = BlockNode()
    footnote_body2 = footnote_block_node2
    fnm.add_body(footnote_name2, footnote_body2)

    footnote_list = FootnotesNode()
    fnm.add_footnotes_list(footnote_list)

    fnm.process()

    assert footnote_node1.public_id == "1"
    assert footnote_node1.internal_id == "XXYY"

    assert footnote_node2.public_id == "2"
    assert footnote_node2.internal_id == "XXYY"

    compare_nodes_sequence(
        footnote_list.footnotes,
        [
            FootnotesItemNode(footnote_node1),
            FootnotesItemNode(footnote_node2),
        ],
    )
