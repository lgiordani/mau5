from unittest.mock import Mock

from mau.environment.environment import Environment
from mau.nodes.node import NodeArguments, NodeInfo
from mau.test_helpers import ATestNode, generate_context
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


def test_generic_node():
    node = ATestNode(
        "Some test content",
        arguments=NodeArguments(
            unnamed_args=["arg1"],
            named_args={"key1": "value1"},
            tags=["tag1"],
            subtype="subtype1",
        ),
        info=NodeInfo(
            context=generate_context(1, 2, 3, 4),
        ),
    )

    bv = BaseVisitor(Environment())
    result = bv.visit(node)

    assert result == {
        "_type": "test",
        "_context": generate_context(1, 2, 3, 4).asdict(),
        "unnamed_args": ["arg1"],
        "named_args": {"key1": "value1"},
        "subtype": "subtype1",
        "tags": ["tag1"],
        "parent": {},
    }
