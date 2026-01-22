from mau.nodes.header import HeaderNode
from mau.nodes.node import NodeInfo
from mau.test_helpers import (
    check_node_with_content,
    check_node_with_labels,
    check_visit_node,
)


def test_header_node_without_content():
    node = HeaderNode(
        level=42,
        internal_id="some_internal_id",
        name="some_alias",
    )

    expected = {
        "_type": "header",
        "level": 42,
        "internal_id": "some_internal_id",
        "name": "some_alias",
        "labels": {},
        "content": [],
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)


def test_header_node_with_content():
    node = HeaderNode(
        level=42,
        internal_id="some_internal_id",
        name="some_alias",
    )

    check_node_with_content(node)


def test_header_node_with_labels():
    node = HeaderNode(
        level=42,
        internal_id="some_internal_id",
        name="some_alias",
    )

    check_node_with_labels(node)
