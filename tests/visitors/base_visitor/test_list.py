from mau.nodes.list import ListItemNode, ListNode
from mau.test_helpers import check_visit_node
from mau.text_buffer import Context


def test_list_item_node():
    node = ListItemNode(3)

    expected = {
        "_type": "list-item",
        "_context": Context.empty().asdict(),
        "content": [],
        "level": 3,
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_list_node():
    node = ListNode(ordered=True)

    expected = {
        "_type": "list",
        "_context": Context.empty().asdict(),
        "content": [],
        "labels": {},
        "ordered": True,
        "main_node": False,
        "start": 1,
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_list_node_unordered():
    node = ListNode(ordered=False)

    expected = {
        "_type": "list",
        "_context": Context.empty().asdict(),
        "content": [],
        "labels": {},
        "ordered": False,
        "main_node": False,
        "start": 1,
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_list_node_parameters():
    node = ListNode(ordered=True, main_node=True, start=42)

    expected = {
        "_type": "list",
        "_context": Context.empty().asdict(),
        "content": [],
        "labels": {},
        "ordered": True,
        "main_node": True,
        "start": 42,
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)
