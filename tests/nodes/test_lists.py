from mau.nodes.lists import ListItemNode, ListNode
from mau.text_buffer import Context


def test_list_item_node():
    node = ListItemNode(3)

    assert node.type == "list_item"
    assert node.level == 3
    assert node.asdict() == {
        "type": "list_item",
        "custom": {
            "content": [],
            "level": 3,
        },
        "info": {
            "context": Context.empty().asdict(),
            "unnamed_args": [],
            "named_args": {},
            "tags": [],
            "subtype": None,
        },
    }


def test_list_node():
    node = ListNode(ordered=True)

    assert node.type == "list"
    assert node.ordered is True
    assert node.main_node is False
    assert node.start == 1
    assert node.asdict() == {
        "type": "list",
        "custom": {
            "content": [],
            "labels": {},
            "ordered": True,
            "main_node": False,
            "start": 1,
        },
        "info": {
            "context": Context.empty().asdict(),
            "unnamed_args": [],
            "named_args": {},
            "tags": [],
            "subtype": None,
        },
    }


def test_list_node_unordered():
    node = ListNode(ordered=False)

    assert node.type == "list"
    assert node.ordered is False
    assert node.main_node is False
    assert node.start == 1
    assert node.asdict() == {
        "type": "list",
        "custom": {
            "content": [],
            "labels": {},
            "ordered": False,
            "main_node": False,
            "start": 1,
        },
        "info": {
            "context": Context.empty().asdict(),
            "unnamed_args": [],
            "named_args": {},
            "tags": [],
            "subtype": None,
        },
    }


def test_list_node_parameters():
    node = ListNode(ordered=True, main_node=True, start=42)

    assert node.type == "list"
    assert node.ordered is True
    assert node.main_node is True
    assert node.start == 42
    assert node.asdict() == {
        "type": "list",
        "custom": {
            "content": [],
            "labels": {},
            "ordered": True,
            "main_node": True,
            "start": 42,
        },
        "info": {
            "context": Context.empty().asdict(),
            "unnamed_args": [],
            "named_args": {},
            "tags": [],
            "subtype": None,
        },
    }
