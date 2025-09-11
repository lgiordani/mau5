from mau.nodes.document import HorizontalRuleNodeContent


def test_horizontal_rule_node_content():
    node_content = HorizontalRuleNodeContent()

    assert node_content.type == "horizontal_rule"
    assert node_content.asdict() == {"type": "horizontal_rule"}
