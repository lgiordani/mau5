from unittest.mock import patch

import pytest

from mau.nodes.block import BlockNodeData
from mau.nodes.commands import FootnotesNodeData
from mau.nodes.footnotes import FootnoteNodeData
from mau.nodes.node import Node
from mau.parsers.base_parser import MauParserException
from mau.parsers.managers.footnotes_manager import FootnotesManager
from mau.test_helpers import compare_asdict_list


def test_footnotes_manager_init():
    fnm = FootnotesManager()

    assert fnm.footnotes == []
    assert fnm.bodies == {}
    assert fnm.footnotes_lists == []


def test_footnotes_manager_add_mention():
    fnm = FootnotesManager()

    footnote_data = FootnoteNodeData("name")

    fnm.add_footnote(footnote_data)

    assert fnm.footnotes == [footnote_data]
    assert fnm.bodies == {}
    assert fnm.footnotes_lists == []


def test_footnotes_manager_add_mentions():
    fnm = FootnotesManager()

    footnote_data = FootnoteNodeData("name")

    fnm.add_footnotes([footnote_data])

    assert fnm.footnotes == [footnote_data]
    assert fnm.bodies == {}
    assert fnm.footnotes_lists == []


def test_footnotes_manager_add_data():
    fnm = FootnotesManager()

    footnote_name = "name"
    footnote_block_data = BlockNodeData(content=[])
    footnote_body = footnote_block_data

    fnm.add_body(footnote_name, footnote_body)

    assert fnm.footnotes == []
    assert fnm.bodies == {footnote_name: footnote_block_data}
    assert fnm.footnotes_lists == []


def test_footnotes_manager_add_data_duplicate_name():
    fnm = FootnotesManager()

    footnote_name = "name"

    footnote_block_data1 = BlockNodeData(content=[])
    footnote_body1 = footnote_block_data1

    footnote_block_data2 = BlockNodeData(content=[])
    footnote_body2 = footnote_block_data2

    fnm.add_body(footnote_name, footnote_body1)

    with pytest.raises(ValueError):
        fnm.add_body(footnote_name, footnote_body2)

    assert fnm.footnotes == []
    assert fnm.bodies == {footnote_name: footnote_block_data1}
    assert fnm.footnotes_lists == []


def test_footnotes_manager_add_footnotes_list():
    fnm = FootnotesManager()

    footnote_list = FootnotesNodeData()

    fnm.add_footnotes_list(footnote_list)

    assert fnm.footnotes == []
    assert fnm.bodies == {}
    assert fnm.footnotes_lists == [footnote_list]


def test_footnotes_manager_update():
    fnm = FootnotesManager()
    footnote_name = "name"

    footnote_data = FootnoteNodeData(footnote_name)
    fnm.add_footnote(footnote_data)

    footnote_block_data = BlockNodeData()
    footnote_body = footnote_block_data
    fnm.add_body(footnote_name, footnote_body)

    footnote_list = FootnotesNodeData()
    fnm.add_footnotes_list(footnote_list)

    other_fnm = FootnotesManager()
    other_fnm.update(fnm)

    assert other_fnm.footnotes == [footnote_data]
    assert other_fnm.bodies == {footnote_name: footnote_block_data}
    assert other_fnm.footnotes_lists == [footnote_list]


@patch("mau.parsers.managers.footnotes_manager.default_footnote_unique_id")
def test_footnotes_manager_process(mock_footnote_unique_id):
    mock_footnote_unique_id.return_value = "XXYY"

    fnm = FootnotesManager()

    footnote_name1 = "footnote_name1"
    footnote_name2 = "footnote_name2"

    footnote_data1 = FootnoteNodeData(footnote_name1)
    fnm.add_footnote(footnote_data1)

    footnote_data2 = FootnoteNodeData(footnote_name2)
    fnm.add_footnote(footnote_data2)

    footnote_block_data1 = BlockNodeData()
    footnote_body1 = footnote_block_data1
    fnm.add_body(footnote_name1, footnote_body1)

    footnote_block_data2 = BlockNodeData()
    footnote_body2 = footnote_block_data2
    fnm.add_body(footnote_name2, footnote_body2)

    footnote_list = FootnotesNodeData()
    fnm.add_footnotes_list(footnote_list)

    fnm.process()

    assert footnote_data1.public_id == "1"
    assert footnote_data1.private_id == "XXYY"

    assert footnote_data2.public_id == "2"
    assert footnote_data2.private_id == "XXYY"

    compare_asdict_list(
        footnote_list.footnotes,
        [footnote_data1, footnote_data2],
    )
