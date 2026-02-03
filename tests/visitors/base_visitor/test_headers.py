from mau.nodes.header import HeaderNode
from mau.test_helpers import (
    check_node_with_content,
    check_node_with_labels,
    check_visit_node,
)
from mau.text_buffer import Context


def test_header_node_without_content():
    node = HeaderNode(
        level=42,
        internal_id="some_internal_id",
        name="some_alias",
    )

    expected = {
        "_type": "header",
        "_context": Context.empty().asdict(),
        "level": 42,
        "internal_id": "some_internal_id",
        "name": "some_alias",
        "labels": {},
        "content": [],
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "unnamed_args": [],
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
