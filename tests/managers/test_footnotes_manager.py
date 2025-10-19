from unittest.mock import patch

import pytest

from mau.nodes.footnotes import FootnoteNodeContent, FootnotesListNodeContent
from mau.nodes.macros import MacroFootnoteNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.base_parser import MauParserException
from mau.parsers.managers.footnotes_manager import FootnotesManager
from mau.test_helpers import compare_nodes, generate_context


def test_footnotes_manager_init():
    fnm = FootnotesManager()

    assert fnm.mentions == []
    assert fnm.data == {}
    assert fnm.footnotes_list_nodes == []


def test_footnotes_manager_add_mention():
    fnm = FootnotesManager()

    footnote_macro_node = Node(content=MacroFootnoteNodeContent("footnote_name"))

    fnm.add_mention(footnote_macro_node)

    assert fnm.mentions == [footnote_macro_node]
    assert fnm.data == {}
    assert fnm.footnotes_list_nodes == []


def test_footnotes_manager_add_mentions():
    fnm = FootnotesManager()

    footnote_macro_node = Node(content=MacroFootnoteNodeContent("footnote_name"))

    fnm.add_mentions([footnote_macro_node])

    assert fnm.mentions == [footnote_macro_node]
    assert fnm.data == {}
    assert fnm.footnotes_list_nodes == []


def test_footnotes_manager_add_data():
    fnm = FootnotesManager()

    footnote_name = "footnote_name"
    footnote_node = Node(
        content=FootnoteNodeContent(footnote_name), children={"content": []}
    )

    fnm.add_data(footnote_node)

    assert fnm.mentions == []
    assert fnm.data == {"footnote_name": footnote_node}
    assert fnm.footnotes_list_nodes == []


def test_footnotes_manager_add_data_duplicate_name():
    fnm = FootnotesManager()

    context1 = generate_context(1, 1, 3, 3)
    context2 = generate_context(2, 2, 4, 4)

    footnote_name = "footnote_name"
    footnote_node1 = Node(
        content=FootnoteNodeContent(footnote_name),
        children={"content": []},
        info=NodeInfo(context=context1),
    )
    footnote_node2 = Node(
        content=FootnoteNodeContent(footnote_name),
        children={"content": []},
        info=NodeInfo(context=context2),
    )

    fnm.add_data(footnote_node1)

    with pytest.raises(MauParserException) as exc:
        fnm.add_data(footnote_node2)

    assert fnm.mentions == []
    assert fnm.data == {"footnote_name": footnote_node1}
    assert fnm.footnotes_list_nodes == []
    assert exc.value.context == context2


def test_footnotes_manager_add_footnotes_list_node():
    fnm = FootnotesManager()

    footnote_list_node = Node(content=FootnotesListNodeContent())

    fnm.add_footnotes_list_node(footnote_list_node)

    assert fnm.mentions == []
    assert fnm.data == {}
    assert fnm.footnotes_list_nodes == [footnote_list_node]


@patch("mau.parsers.managers.footnotes_manager.default_footnote_unique_id")
def test_footnotes_manager_process(mock_footnote_unique_id):
    mock_footnote_unique_id.return_value = "XXYY"

    fnm = FootnotesManager()

    footnote_name1 = "footnote_name1"
    footnote_name2 = "footnote_name2"

    footnote_macro_node1 = Node(content=MacroFootnoteNodeContent(footnote_name1))
    fnm.add_mention(footnote_macro_node1)

    footnote_macro_node2 = Node(content=MacroFootnoteNodeContent(footnote_name2))
    fnm.add_mention(footnote_macro_node2)

    footnote_node1 = Node(
        content=FootnoteNodeContent(footnote_name1), children={"content": []}
    )
    fnm.add_data(footnote_node1)

    footnote_node2 = Node(
        content=FootnoteNodeContent(footnote_name2), children={"content": []}
    )
    fnm.add_data(footnote_node2)

    footnote_list_node = Node(content=FootnotesListNodeContent())

    fnm.add_footnotes_list_node(footnote_list_node)

    fnm.process()

    assert footnote_macro_node1.content.public_id == "1"
    assert footnote_node1.content.public_id == "1"
    assert footnote_macro_node1.content.private_id == "XXYY"
    assert footnote_node1.content.private_id == "XXYY"

    assert footnote_macro_node2.content.public_id == "2"
    assert footnote_node2.content.public_id == "2"
    assert footnote_macro_node2.content.private_id == "XXYY"
    assert footnote_node2.content.private_id == "XXYY"

    assert footnote_macro_node1.children["footnote"] == [footnote_node1]
    assert footnote_macro_node2.children["footnote"] == [footnote_node2]

    compare_nodes(
        footnote_list_node.children["entries"], [footnote_node1, footnote_node2]
    )
