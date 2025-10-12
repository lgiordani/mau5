from mau.nodes.document import (
    ContainerNodeContent,
    DocumentNodeContent,
    HorizontalRuleNodeContent,
    WrapperNodeContent,
)


def test_horizontal_rule_node_content():
    node_content = HorizontalRuleNodeContent()

    assert node_content.type == "horizontal_rule"
    assert node_content.asdict() == {"type": "horizontal_rule"}


def test_wrapper_node_content():
    node_content = WrapperNodeContent()

    assert node_content.type == "wrapper"
    assert node_content.asdict() == {"type": "wrapper"}


def test_document_node_content():
    node_content = DocumentNodeContent()

    assert node_content.type == "document"
    assert node_content.asdict() == {"type": "document"}


def test_container_node_content():
    node_content = ContainerNodeContent("somelabel")

    assert node_content.type == "container"
    assert node_content.asdict() == {"type": "container", "label": "somelabel"}
