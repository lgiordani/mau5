from unittest.mock import Mock

from mau.nodes.node import Node, NodeContent, NodeInfo, ValueNodeContent
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
        "context": generate_context(0, 0, 0, 0),
        "unnamed_args": ["arg1"],
        "named_args": {"key1": "value1"},
        "tags": ["tag1"],
        "subtype": "subtype1",
    }


def test_node():
    node = Node(content=NodeContent())

    assert node.parent is None
    assert node.children == {}

    assert node.content.asdict() == {"type": "none"}

    assert node.asdict() == {
        "children": {},
        "content": {"type": "none"},
        "info": {
            "context": Context.empty(),
            "unnamed_args": [],
            "named_args": {},
            "tags": [],
            "subtype": None,
        },
    }


def test_node_children():
    mock_node = Mock()

    node = Node(content=NodeContent())
    node.add_children({"title": [mock_node]})

    assert node.parent is None
    assert node.children == {"title": [mock_node]}

    assert node.content.asdict() == {"type": "none"}

    assert node.asdict() == {
        "children": {"title": [mock_node.asdict()]},
        "content": {"type": "none"},
        "info": {
            "context": Context.empty(),
            "unnamed_args": [],
            "named_args": {},
            "tags": [],
            "subtype": None,
        },
    }

    mock_node.set_parent.assert_called_with(node)


def test_node_parent():
    parent = Node(content=NodeContent())
    node = Node(parent=parent)

    assert node.parent is parent


def test_node_set_parent():
    parent = Node(content=NodeContent())
    node = Node(content=NodeContent())

    node.set_parent(parent)

    assert node.parent is parent


def test_node_equality():
    node1 = Node(content=NodeContent())
    node2 = Node(content=NodeContent())

    assert node1 == node2


def test_node_equality_with_non_node():
    node1 = Node(content=NodeContent())

    assert node1 != NodeContent()


def test_node_add_children():
    child1 = Node(content=NodeContent())
    child2 = Node(content=NodeContent())
    node = Node(content=NodeContent(), children={"content": [child1]})

    node.add_children({"content": [child2]})

    assert len(node.children["content"]) == 2
    assert child1.parent is node
    assert child2.parent is node


def test_node_add_children_at_existing_position():
    child1 = Node(content=NodeContent())
    child2 = Node(content=NodeContent())
    node = Node(content=NodeContent(), children={"content": [child1]})

    node.add_children_at_position("content", [child2])

    assert len(node.children["content"]) == 2
    assert child1.parent is node
    assert child2.parent is node


def test_node_add_children_at_non_existing_position():
    child1 = Node(content=NodeContent())
    child2 = Node(content=NodeContent())
    node = Node(content=NodeContent(), children={"content": [child1]})

    node.add_children_at_position("title", [child2])

    assert len(node.children["content"]) == 1
    assert len(node.children["title"]) == 1
    assert child1.parent is node
    assert child2.parent is node


def test_value_node_content():
    content = ValueNodeContent(value="somevalue")

    assert content.type == "value"
    assert content.value == "somevalue"
    assert content.asdict() == {"type": "value", "value": "somevalue"}


def test_node_check_children_allowed():
    class TestNodeContent(NodeContent):
        type = "test"
        allowed_keys = {"content": "Some description"}

    node = Node(content=TestNodeContent(), children={"content": []})

    assert node.check_children() == set()


def test_node_check_children_not_allowed():
    class TestNodeContent(NodeContent):
        type = "test"
        allowed_keys = {"content": "Some description"}

    node = Node(content=TestNodeContent(), children={"title": []})

    assert node.check_children() == {"title"}


def test_node_check_children_allow_all():
    class TestNodeContent(NodeContent):
        type = "test"
        allowed_keys = {}

    node = Node(content=TestNodeContent())
    node.add_children(children={"content": []}, allow_all=True)

    assert node.check_children() == set()
    assert node.allowed_keys == {"content": "Dynamically added children"}
