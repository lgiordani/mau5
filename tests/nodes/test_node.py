from mau.nodes.node import Node, NodeInfo, WrapperNode
from mau.test_helpers import generate_context
from mau.text_buffer import Context


def test_info():
    info = NodeInfo(
        context=generate_context(0, 0, 0, 0),
        unnamed_args=["arg1"],
        named_args={"key1": "value1"},
        tags=["tag1"],
        subtype="subtype1",
    )

    assert info.asdict() == {
        "context": generate_context(0, 0, 0, 0).asdict(),
        "unnamed_args": ["arg1"],
        "named_args": {"key1": "value1"},
        "tags": ["tag1"],
        "subtype": "subtype1",
    }


def test_node():
    node = Node()

    assert node.parent is None
    assert node.asdict() == {
        "type": "none",
        "custom": {},
        "info": {
            "context": Context.empty().asdict(),
            "unnamed_args": [],
            "named_args": {},
            "tags": [],
            "subtype": None,
        },
    }


def test_node_with_info():
    info = NodeInfo(
        context=generate_context(0, 0, 0, 0),
        unnamed_args=["arg1"],
        named_args={"key1": "value1"},
        tags=["tag1"],
        subtype="subtype1",
    )

    node = Node(info=info)

    assert node.asdict() == {
        "type": "none",
        "custom": {},
        "info": {
            "context": generate_context(0, 0, 0, 0).asdict(),
            "unnamed_args": ["arg1"],
            "named_args": {"key1": "value1"},
            "tags": ["tag1"],
            "subtype": "subtype1",
        },
    }


def test_node_parent():
    parent = Node()
    node = Node(parent=parent)

    assert node.parent is parent


def test_node_set_parent():
    parent = Node()
    node = Node()

    node.set_parent(parent)

    assert node.parent is parent


def test_node_equality():
    node1 = Node()
    node2 = Node()

    assert node1 == node2


def test_node_equality_with_non_node():
    node = Node()

    assert node != 42


def test_wrapper_node():
    node = WrapperNode()

    assert node.type == "wrapper"
    assert node.asdict() == {
        "type": "wrapper",
        "custom": {
            "content": [],
        },
        "info": {
            "context": Context.empty().asdict(),
            "unnamed_args": [],
            "named_args": {},
            "tags": [],
            "subtype": None,
        },
    }
