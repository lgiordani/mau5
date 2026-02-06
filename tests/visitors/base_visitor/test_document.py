from mau.nodes.document import (
    DocumentNode,
    HorizontalRuleNode,
)
from mau.test_helpers import check_visit_node
from mau.text_buffer import Context


def test_horizontal_rule_node():
    node = HorizontalRuleNode()

    expected = {
        "_type": "horizontal-rule",
        "_context": Context.empty().asdict(),
        "labels": {},
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "internal_tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_document_node():
    node = DocumentNode()

    expected = {
        "_type": "document",
        "_context": Context.empty().asdict(),
        "content": [],
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "internal_tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)
