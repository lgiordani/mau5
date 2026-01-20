from mau.nodes.list import ListItemNode, ListNode
from mau.nodes.node import NodeInfo
from mau.test_helpers import check_visit_node


def test_list_item_node():
    node = ListItemNode(3)

    expected = {
        "_type": "list-item",
        "content": [],
        "level": 3,
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)


def test_list_node():
    node = ListNode(ordered=True)

    expected = {
        "_type": "list",
        "content": [],
        "labels": {},
        "ordered": True,
        "main_node": False,
        "start": 1,
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)


def test_list_node_unordered():
    node = ListNode(ordered=False)

    expected = {
        "_type": "list",
        "content": [],
        "labels": {},
        "ordered": False,
        "main_node": False,
        "start": 1,
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)


def test_list_node_parameters():
    node = ListNode(ordered=True, main_node=True, start=42)

    expected = {
        "_type": "list",
        "content": [],
        "labels": {},
        "ordered": True,
        "main_node": True,
        "start": 42,
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)
