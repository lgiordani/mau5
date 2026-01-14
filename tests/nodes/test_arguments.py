# from mau.nodes.arguments import NamedArgumentNodeData, UnnamedArgumentNodeData
# 
# 
# def test_unnamed_argument_node_content():
#     node_content = UnnamedArgumentNodeData("somevalue")
# 
#     assert node_content.type == "unnamed_argument"
#     assert node_content.value == "somevalue"
#     assert node_content.asdict() == {
#         "type": "unnamed_argument",
#         "custom": {
#             "value": "somevalue",
#         },
#     }
# 
# 
# def test_named_argument_node_content():
#     node_content = NamedArgumentNodeData("somekey", "somevalue")
# 
#     assert node_content.type == "named_argument"
#     assert node_content.key == "somekey"
#     assert node_content.value == "somevalue"
#     assert node_content.asdict() == {
#         "custom": {
#             "key": "somekey",
#             "value": "somevalue",
#         },
#         "type": "named_argument",
#     }
