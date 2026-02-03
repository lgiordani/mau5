from mau.nodes.node import Node, NodeInfo
from mau.nodes.node_arguments import NodeArguments
from mau.test_helpers import generate_context


def test_info():
    info = NodeInfo(
        context=generate_context(0, 0, 0, 0),
    )

    assert info.asdict() == {
        "context": generate_context(0, 0, 0, 0).asdict(),
    }


def test_arguments():
    arguments = NodeArguments(
        unnamed_args=["arg1"],
        named_args={"key1": "value1"},
        tags=["tag1"],
        subtype="subtype1",
    )

    assert arguments.asdict() == {
        "unnamed_args": ["arg1"],
        "named_args": {"key1": "value1"},
        "tags": ["tag1"],
        "subtype": "subtype1",
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
