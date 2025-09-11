from unittest.mock import Mock

from mau.nodes.node import Node, NodeContent, NodeInfo, ValueNodeContent
from mau.test_helpers import generate_context


def test_info():
    info = NodeInfo(
        context=generate_context(0, 0),
        position="title",
        unnamed_args=["arg1"],
        named_args={"key1": "value1"},
        tags=["tag1"],
        subtype="subtype1",
    )

    assert info.asdict() == {
        "context": generate_context(0, 0),
        "position": "title",
        "unnamed_args": ["arg1"],
        "named_args": {"key1": "value1"},
        "tags": ["tag1"],
        "subtype": "subtype1",
    }


def test_info_set_position():
    info = NodeInfo()
    info.set_position("top")

    assert info.position == "top"


def test_info_set_context():
    info = NodeInfo()
    info.set_context(generate_context(0, 0))

    assert info.context == generate_context(0, 0)


def test_node():
    node = Node()

    assert node.parent is None
    assert node.children == {}
    assert node.info.position is None

    assert node.content.asdict() == {"type": "none"}

    assert node.asdict() == {
        "children": {},
        "content": {"type": "none"},
        "info": {
            "context": None,
            "position": None,
            "unnamed_args": [],
            "named_args": {},
            "tags": [],
            "subtype": None,
        },
    }


def test_node_children():
    mock_node = Mock()

    node = Node()
    node.add_children({"title": [mock_node]})

    assert node.parent is None
    assert node.children == {"title": [mock_node]}
    assert node.info.position is None

    assert node.content.asdict() == {"type": "none"}

    assert node.asdict() == {
        "children": {"title": [mock_node.asdict()]},
        "content": {"type": "none"},
        "info": {
            "context": None,
            "position": None,
            "unnamed_args": [],
            "named_args": {},
            "tags": [],
            "subtype": None,
        },
    }

    mock_node.set_parent.assert_called_with(node)


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


def test_node_add_children():
    child1 = Node()
    child2 = Node()
    node = Node(children={"content": [child1]})

    node.add_children({"content": [child2]})

    assert len(node.children["content"]) == 2
    assert child1.parent is node
    assert child2.parent is node


def test_node_add_children_at_existing_position():
    child1 = Node()
    child2 = Node()
    node = Node(children={"content": [child1]})

    node.add_children_at_position("content", [child2])

    assert len(node.children["content"]) == 2
    assert child1.parent is node
    assert child2.parent is node


def test_node_add_children_at_non_existing_position():
    child1 = Node()
    child2 = Node()
    node = Node(children={"content": [child1]})

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


# def test_node_accept():
#     visitor = Mock()
#     node = Node()
#     node.node_type = "mynode"

#     assert node.accept(visitor) == visitor._visit_mynode()


# def test_node_accept_default():
#     # This makes the Mock raise an AttributeError
#     # for anything that is not in the list
#     visitor = Mock(spec=["_visit_default"])
#     node = Node()
#     node.node_type = "mynode"

#     assert node.accept(visitor) == visitor._visit_default()
