# from mau.nodes.document import (
#     ContainerNodeData,
#     DocumentNodeData,
#     HorizontalRuleNodeData,
#     WrapperNodeData,
# )


# def test_horizontal_rule_node_content():
#     node_content = HorizontalRuleNodeData()

#     assert node_content.type == "horizontal_rule"
#     assert node_content.asdict() == {"type": "horizontal_rule"}


# def test_wrapper_node_content():
#     node_content = WrapperNodeData()

#     assert node_content.type == "wrapper"
#     assert node_content.asdict() == {"type": "wrapper"}


# def test_document_node_content():
#     node_content = DocumentNodeData()

#     assert node_content.type == "document"
#     assert node_content.asdict() == {"type": "document"}


# def test_container_node_content():
#     node_content = ContainerNodeData("somelabel")

#     assert node_content.type == "container"
#     assert node_content.asdict() == {"type": "container", "label": "somelabel"}
