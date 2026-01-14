# from mau.nodes.node import Node, NodeData, NodeInfo, WrapperNodeData
# from mau.test_helpers import generate_context
# from mau.text_buffer import Context
# 
# 
# def test_info():
#     info = NodeInfo(
#         context=generate_context(0, 0, 0, 0),
#         unnamed_args=["arg1"],
#         named_args={"key1": "value1"},
#         tags=["tag1"],
#         subtype="subtype1",
#     )
# 
#     assert info.asdict() == {
#         "context": generate_context(0, 0, 0, 0).asdict(),
#         "unnamed_args": ["arg1"],
#         "named_args": {"key1": "value1"},
#         "tags": ["tag1"],
#         "subtype": "subtype1",
#     }
# 
# 
# def test_node():
#     node = Node(data=NodeData())
# 
#     assert node.parent is None
# 
#     assert node.data.asdict() == {"type": "none", "custom": {}}
#     assert node.tags == []
# 
#     assert node.asdict() == {
#         "data": {"type": "none", "custom": {}},
#         "info": {
#             "context": Context.empty().asdict(),
#             "unnamed_args": [],
#             "named_args": {},
#             "tags": [],
#             "subtype": None,
#         },
#     }
# 
# 
# def test_node_with_info():
#     info = NodeInfo(
#         context=generate_context(0, 0, 0, 0),
#         unnamed_args=["arg1"],
#         named_args={"key1": "value1"},
#         tags=["tag1"],
#         subtype="subtype1",
#     )
# 
#     node = Node(data=NodeData(), info=info)
# 
#     assert node.tags == ["tag1"]
# 
#     assert node.asdict() == {
#         "data": {"type": "none", "custom": {}},
#         "info": {
#             "context": generate_context(0, 0, 0, 0).asdict(),
#             "unnamed_args": ["arg1"],
#             "named_args": {"key1": "value1"},
#             "tags": ["tag1"],
#             "subtype": "subtype1",
#         },
#     }
# 
# 
# def test_node_parent():
#     parent = Node(data=NodeData())
#     node = Node(data=NodeData(), parent=parent)
# 
#     assert node.parent is parent
# 
# 
# def test_node_set_parent():
#     parent = Node(data=NodeData())
#     node = Node(data=NodeData())
# 
#     node.set_parent(parent)
# 
#     assert node.parent is parent
# 
# 
# def test_node_equality():
#     node1 = Node(data=NodeData())
#     node2 = Node(data=NodeData())
# 
#     assert node1 == node2
# 
# 
# def test_node_equality_with_non_node():
#     node1 = Node(data=NodeData())
# 
#     assert node1 != NodeData()
# 
# 
# def test_wrapper_node_content():
#     node_content = WrapperNodeData()
# 
#     assert node_content.type == "wrapper"
#     assert node_content.asdict() == {
#         "type": "wrapper",
#         "custom": {
#             "content": [],
#         },
#     }
