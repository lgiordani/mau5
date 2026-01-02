from unittest.mock import Mock

from mau.environment.environment import Environment
from mau.nodes.inline import TextNodeContent
from mau.nodes.node import Node, NodeInfo, ValueNodeContent
from mau.nodes.paragraph import ParagraphNodeContent
from mau.test_helpers import generate_context
from mau.visitors.base_visitor import BaseVisitor


def test_visitor_node_accept():
    node = Mock()

    bv = BaseVisitor(Environment())
    result = bv.visit(node, "arg1", key1="value1")

    node.accept.assert_called_with(bv, "arg1", key1="value1")
    assert result == node.accept.return_value


def test_visitor_no_node():
    bv = BaseVisitor(Environment())
    result = bv.visit(None, "arg1", key1="value1")

    assert result == {}


def test_unknown_node():
    class TestNodeContent(ValueNodeContent):
        type = "test"

    node = Node(
        content=TestNodeContent("Some test content"),
        info=NodeInfo(
            unnamed_args=["arg1"],
            named_args={"key1": "value1"},
            tags=["tag1"],
            subtype="subtype1",
            context=generate_context(1, 2, 3, 4),
        ),
    )

    bv = BaseVisitor(Environment())
    result = bv.visit(node)

    assert result == {
        "children": {},
        "content": {"type": "test", "value": "Some test content"},
        "info": {
            "unnamed_args": ["arg1"],
            "named_args": {"key1": "value1"},
            "subtype": "subtype1",
            "tags": ["tag1"],
            "context": generate_context(1, 2, 3, 4).asdict(),
        },
    }


def test_unknown_node_with_children():
    class TestNodeContent(ValueNodeContent):
        type = "test"

    child1 = Node(
        content=TestNodeContent("Child 1 content"),
        info=NodeInfo(context=generate_context(0, 0, 0, 0)),
    )

    child2 = Node(
        content=TestNodeContent("Child 2 content"),
        info=NodeInfo(context=generate_context(0, 0, 0, 0)),
    )

    child3 = Node(
        content=TestNodeContent("Child 3 content"),
        info=NodeInfo(context=generate_context(0, 0, 0, 0)),
    )

    node = Node(
        content=TestNodeContent("Parent content"),
        children={"group1": [child1], "group2": [child2, child3]},
        info=NodeInfo(context=generate_context(0, 0, 0, 0)),
    )

    bv = BaseVisitor(Environment())
    result = bv.visit(node)

    assert result == {
        "children": {
            "group1": [
                {
                    "children": {},
                    "content": {"type": "test", "value": "Child 1 content"},
                    "info": {
                        "unnamed_args": [],
                        "named_args": {},
                        "subtype": None,
                        "tags": [],
                        "context": generate_context(0, 0, 0, 0).asdict(),
                    },
                }
            ],
            "group2": [
                {
                    "children": {},
                    "content": {"type": "test", "value": "Child 2 content"},
                    "info": {
                        "unnamed_args": [],
                        "named_args": {},
                        "subtype": None,
                        "tags": [],
                        "context": generate_context(0, 0, 0, 0).asdict(),
                    },
                },
                {
                    "children": {},
                    "content": {"type": "test", "value": "Child 3 content"},
                    "info": {
                        "unnamed_args": [],
                        "named_args": {},
                        "subtype": None,
                        "tags": [],
                        "context": generate_context(0, 0, 0, 0).asdict(),
                    },
                },
            ],
        },
        "content": {"type": "test", "value": "Parent content"},
        "info": {
            "unnamed_args": [],
            "named_args": {},
            "subtype": None,
            "tags": [],
            "context": generate_context(0, 0, 0, 0).asdict(),
        },
    }


def test_paragraph_node():
    node = Node(
        content=ParagraphNodeContent(),
        children={
            "title": [
                Node(
                    content=TextNodeContent("Some title"),
                    info=NodeInfo(context=generate_context(1, 2, 3, 4)),
                )
            ],
            "content": [
                Node(
                    content=TextNodeContent("Just some text"),
                    info=NodeInfo(context=generate_context(2, 3, 4, 5)),
                )
            ],
        },
        info=NodeInfo(
            unnamed_args=["arg1"],
            named_args={"key1": "value1"},
            tags=["tag1"],
            subtype="subtype1",
            context=generate_context(3, 4, 5, 6),
        ),
    )

    bv = BaseVisitor(Environment())
    result = bv.visit(node)

    assert result == {
        "children": {
            "title": [
                {
                    "children": {},
                    "content": {"type": "text", "value": "Some title"},
                    "info": {
                        "unnamed_args": [],
                        "named_args": {},
                        "subtype": None,
                        "tags": [],
                        "context": generate_context(1, 2, 3, 4).asdict(),
                    },
                }
            ],
            "content": [
                {
                    "children": {},
                    "content": {"type": "text", "value": "Just some text"},
                    "info": {
                        "unnamed_args": [],
                        "named_args": {},
                        "subtype": None,
                        "tags": [],
                        "context": generate_context(2, 3, 4, 5).asdict(),
                    },
                },
            ],
        },
        "content": {"type": "paragraph"},
        "info": {
            "unnamed_args": ["arg1"],
            "named_args": {"key1": "value1"},
            "subtype": "subtype1",
            "tags": ["tag1"],
            "context": generate_context(3, 4, 5, 6).asdict(),
        },
    }
