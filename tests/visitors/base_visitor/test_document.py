from mau.nodes.document import (
    DocumentNode,
    HorizontalRuleNode,
)
from mau.nodes.node import NodeInfo
from mau.test_helpers import check_visit_node


def test_horizontal_rule_node():
    node = HorizontalRuleNode()

    expected = {
        "_type": "horizontal-rule",
        "_parent_info": {},
        "_info": NodeInfo.empty().asdict(),
        "labels": {},
    }

    check_visit_node(node, expected)


def test_document_node():
    node = DocumentNode()

    expected = {
        "_type": "document",
        "_parent_info": {},
        "_info": NodeInfo.empty().asdict(),
        "content": [],
    }

    check_visit_node(node, expected)
