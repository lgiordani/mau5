# from mau.nodes.lists import ListItemNodeData, ListNodeData
# 
# 
# def test_list_item_node_content():
#     node_content = ListItemNodeData(3)
# 
#     assert node_content.type == "list_item"
#     assert node_content.level == 3
#     assert node_content.asdict() == {
#         "type": "list_item",
#         "custom": {
#             "content": [],
#             "level": 3,
#         },
#     }
# 
# 
# def test_list_node_content():
#     node_content = ListNodeData(ordered=True)
# 
#     assert node_content.type == "list"
#     assert node_content.ordered is True
#     assert node_content.main_node is False
#     assert node_content.start == 1
#     assert node_content.asdict() == {
#         "type": "list",
#         "custom": {
#             "content": [],
#             "labels": {},
#             "ordered": True,
#             "main_node": False,
#             "start": 1,
#         },
#     }
# 
# 
# def test_list_node_content_unordered():
#     node_content = ListNodeData(ordered=False)
# 
#     assert node_content.type == "list"
#     assert node_content.ordered is False
#     assert node_content.main_node is False
#     assert node_content.start == 1
#     assert node_content.asdict() == {
#         "type": "list",
#         "custom": {
#             "content": [],
#             "labels": {},
#             "ordered": False,
#             "main_node": False,
#             "start": 1,
#         },
#     }
# 
# 
# def test_list_node_content_parameters():
#     node_content = ListNodeData(ordered=True, main_node=True, start=42)
# 
#     assert node_content.type == "list"
#     assert node_content.ordered is True
#     assert node_content.main_node is True
#     assert node_content.start == 42
#     assert node_content.asdict() == {
#         "type": "list",
#         "custom": {
#             "content": [],
#             "labels": {},
#             "ordered": True,
#             "main_node": True,
#             "start": 42,
#         },
#     }
