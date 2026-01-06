from unittest.mock import call, patch

from mau.nodes.commands import (
    TocItemNodeData,
    TocNodeData,
)
from mau.nodes.headers import HeaderNodeData
from mau.nodes.inline import TextNodeData
from mau.nodes.node import Node, NodeInfo
from mau.parsers.managers.toc_manager import (
    TocManager,
    add_nodes_under_level,
)
from mau.test_helpers import generate_context, compare_asdict_list


def test_toc_manager_init():
    tm = TocManager()

    assert tm.headers == []
    assert tm.toc_nodes == []


def test_toc_manager_add_header():
    tm = TocManager()
    header_data = HeaderNodeData(level=1)

    tm.add_header(header_data)

    assert tm.headers == [header_data]


def test_toc_manager_add_toc_node():
    tm = TocManager()
    toc_data = TocNodeData()

    tm.add_toc_node(toc_data)

    assert tm.toc_nodes == [toc_data]


def test_toc_manager_update():
    tm = TocManager()
    header_data = HeaderNodeData(1)
    toc_data = TocNodeData()
    tm.add_header(header_data)
    tm.add_toc_node(toc_data)

    other_tm = TocManager()
    other_tm.update(tm)

    assert other_tm.headers == [header_data]
    assert other_tm.toc_nodes == [toc_data]


def test_add_nodes_without_nesting():
    node_header_a = HeaderNodeData(1, "A")
    node_header_b = HeaderNodeData(1, "B")
    node_header_c = HeaderNodeData(1, "C")

    node_toc_item_a = TocItemNodeData(node_header_a)
    node_toc_item_b = TocItemNodeData(node_header_b)
    node_toc_item_c = TocItemNodeData(node_header_c)

    nodes = [
        node_header_a,
        node_header_b,
        node_header_c,
    ]

    children: list[TocItemNodeData] = []

    idx = add_nodes_under_level(0, nodes, 0, children)

    assert idx == len(nodes)

    compare_asdict_list(children, [node_toc_item_a, node_toc_item_b, node_toc_item_c])


def test_add_nodes_with_nesting():
    node_header_a = HeaderNodeData(1, "A")
    node_header_b = HeaderNodeData(2, "B")
    node_header_c = HeaderNodeData(3, "C")
    node_header_d = HeaderNodeData(2, "D")
    node_header_e = HeaderNodeData(2, "E")
    node_header_f = HeaderNodeData(1, "F")
    node_header_g = HeaderNodeData(3, "G")

    node_toc_item_c = TocItemNodeData(node_header_c)
    node_toc_item_b = TocItemNodeData(node_header_b, entries=[node_toc_item_c])
    node_toc_item_d = TocItemNodeData(node_header_d)
    node_toc_item_e = TocItemNodeData(node_header_e)
    node_toc_item_a = TocItemNodeData(
        node_header_a, entries=[node_toc_item_b, node_toc_item_d, node_toc_item_e]
    )
    node_toc_item_g = TocItemNodeData(node_header_g)
    node_toc_item_f = TocItemNodeData(node_header_f, entries=[node_toc_item_g])

    nodes = [
        node_header_a,
        node_header_b,
        node_header_c,
        node_header_d,
        node_header_e,
        node_header_f,
        node_header_g,
    ]

    children: list[TocItemNodeData] = []

    idx = add_nodes_under_level(0, nodes, 0, children)

    assert idx == len(nodes)

    compare_asdict_list(children, [node_toc_item_a, node_toc_item_f])


def test_add_nodes_under_level_starts_with_any_level():
    node_header_a = HeaderNodeData(3, "A")
    node_header_b = HeaderNodeData(2, "B")
    node_header_c = HeaderNodeData(3, "C")

    node_toc_item_c = TocItemNodeData(node_header_c)
    node_toc_item_b = TocItemNodeData(node_header_b, entries=[node_toc_item_c])
    node_toc_item_a = TocItemNodeData(node_header_a)

    nodes = [
        node_header_a,
        node_header_b,
        node_header_c,
    ]

    children: list[TocItemNodeData] = []

    idx = add_nodes_under_level(0, nodes, 0, children)

    assert idx == len(nodes)

    compare_asdict_list(children, [node_toc_item_a, node_toc_item_b])


def test_add_nodes_under_level_can_terminate_with_single_node():
    node_header_a = HeaderNodeData(3, "A")
    node_header_b = HeaderNodeData(2, "B")
    node_header_c = HeaderNodeData(1, "C")

    node_toc_item_a = TocItemNodeData(node_header_a)
    node_toc_item_b = TocItemNodeData(node_header_b)
    node_toc_item_c = TocItemNodeData(node_header_c)

    nodes = [
        node_header_a,
        node_header_b,
        node_header_c,
    ]

    children: list[TocItemNodeData] = []

    idx = add_nodes_under_level(0, nodes, 0, children)

    assert idx == len(nodes)

    compare_asdict_list(children, [node_toc_item_a, node_toc_item_b, node_toc_item_c])


@patch("mau.parsers.managers.toc_manager.default_header_internal_id")
def test_process(mock_default_header_internal_id):
    mock_default_header_internal_id.return_value = "some_uid"

    node_header_a = HeaderNodeData(1)
    node_header_b = HeaderNodeData(2)

    node_toc_item_b = TocItemNodeData(node_header_b)
    node_toc_item_a = TocItemNodeData(node_header_a, entries=[node_toc_item_b])

    header_nodes = [
        node_header_a,
        node_header_b,
    ]

    tm = TocManager()
    tm.headers = header_nodes
    test_toc_node = TocNodeData()
    tm.add_toc_node(test_toc_node)

    tm.process()

    compare_asdict_list(test_toc_node.plain_entries, header_nodes)
    compare_asdict_list(test_toc_node.nested_entries, [node_toc_item_a])

    assert mock_default_header_internal_id.mock_calls == [
        call(node_header_a),
        call(node_header_b),
    ]


def test_process_internal_id():
    node_header_a = HeaderNodeData(1, "A")
    node_header_b = HeaderNodeData(2, "B")

    node_toc_item_b = TocItemNodeData(node_header_b)
    node_toc_item_a = TocItemNodeData(node_header_a, entries=[node_toc_item_b])

    header_nodes = [
        node_header_a,
        node_header_b,
    ]

    tm = TocManager()
    tm.headers = header_nodes
    test_toc_node = TocNodeData()
    tm.add_toc_node(test_toc_node)

    tm.process()

    compare_asdict_list(test_toc_node.plain_entries, header_nodes)
    compare_asdict_list(test_toc_node.nested_entries, [node_toc_item_a])
