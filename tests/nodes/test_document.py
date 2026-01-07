from mau.nodes.document import (
    DocumentNodeData,
    HorizontalRuleNodeData,
)


def test_horizontal_rule_node_content():
    node_content = HorizontalRuleNodeData()

    assert node_content.type == "horizontal_rule"
    assert node_content.asdict() == {
        "type": "horizontal_rule",
        "custom": {
            "labels": {},
        },
    }


def test_document_node_content():
    node_content = DocumentNodeData()

    assert node_content.type == "document"
    assert node_content.asdict() == {
        "type": "document",
        "custom": {
            "content": [],
        },
    }
