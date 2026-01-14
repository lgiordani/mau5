# from mau.nodes.node import Node
# from mau.nodes.block import BlockNodeData
# from mau.nodes.commands import FootnotesNodeData, TocItemNodeData
# from mau.nodes.footnotes import FootnoteNodeData
# from mau.nodes.headers import HeaderNodeData
# from mau.nodes.commands import BlockGroupNodeData
# 
# 
# def test_footnotes_node_content_empty():
#     node_data = FootnotesNodeData()
# 
#     assert node_data.type == "footnotes"
#     assert node_data.footnotes == []
# 
#     assert node_data.asdict() == {
#         "type": "footnotes",
#         "custom": {"footnotes": [], "labels": {}},
#     }
# 
# 
# def test_footnotes_node_content():
#     footnotes = [
#         FootnoteNodeData("somename1"),
#         FootnoteNodeData("somename2"),
#     ]
#     node_data = FootnotesNodeData(footnotes=footnotes)
# 
#     assert node_data.type == "footnotes"
#     assert node_data.footnotes == footnotes
# 
#     assert node_data.asdict() == {
#         "type": "footnotes",
#         "custom": {
#             "footnotes": [
#                 {
#                     "type": "footnote",
#                     "custom": {
#                         "name": "somename1",
#                         "public_id": None,
#                         "private_id": None,
#                         "content": [],
#                     },
#                 },
#                 {
#                     "type": "footnote",
#                     "custom": {
#                         "name": "somename2",
#                         "public_id": None,
#                         "private_id": None,
#                         "content": [],
#                     },
#                 },
#             ],
#             "labels": {},
#         },
#     }
# 
# 
# def test_toc_item_node_data_without_entries():
#     toc_item_data = TocItemNodeData(
#         header=HeaderNodeData(level=1),
#         entries=[],
#     )
# 
#     assert toc_item_data.type == "toc.item"
#     assert toc_item_data.entries == []
# 
#     assert toc_item_data.asdict() == {
#         "type": "toc.item",
#         "custom": {
#             "entries": [],
#             "header": {
#                 "type": "header",
#                 "custom": {
#                     "level": 1,
#                     "internal_id": None,
#                     "alias": None,
#                     "labels": {},
#                     "content": [],
#                 },
#             },
#         },
#     }
# 
# 
# def test_toc_item_node_data_with_entries():
#     toc_item_data_child = TocItemNodeData(
#         header=HeaderNodeData(level=2),
#         entries=[],
#     )
# 
#     toc_item_data = TocItemNodeData(
#         header=HeaderNodeData(level=1),
#         entries=[toc_item_data_child],
#     )
# 
#     assert toc_item_data.type == "toc.item"
#     assert toc_item_data.entries == [toc_item_data_child]
# 
#     assert toc_item_data.asdict() == {
#         "type": "toc.item",
#         "custom": {
#             "entries": [
#                 {
#                     "type": "toc.item",
#                     "custom": {
#                         "entries": [],
#                         "header": {
#                             "type": "header",
#                             "custom": {
#                                 "level": 2,
#                                 "internal_id": None,
#                                 "alias": None,
#                                 "labels": {},
#                                 "content": [],
#                             },
#                         },
#                     },
#                 }
#             ],
#             "header": {
#                 "type": "header",
#                 "custom": {
#                     "level": 1,
#                     "internal_id": None,
#                     "alias": None,
#                     "labels": {},
#                     "content": [],
#                 },
#             },
#         },
#     }
# 
# 
# def test_block_group_node_data_empty():
#     node_data = BlockGroupNodeData("somename")
# 
#     assert node_data.type == "block-group"
#     assert node_data.asdict() == {
#         "type": "block-group",
#         "custom": {
#             "name": "somename",
#             "blocks": {},
#             "labels": {},
#         },
#     }
# 
# 
# def test_block_group_node_data_with_blocks():
#     block_data1 = BlockNodeData()
#     block_node1 = Node(data=block_data1)
#     block_data2 = BlockNodeData()
#     block_node2 = Node(data=block_data2)
# 
#     node_data = BlockGroupNodeData(
#         "somename", blocks={"position1": block_node1, "position2": block_node2}
#     )
# 
#     assert node_data.type == "block-group"
#     assert node_data.asdict() == {
#         "type": "block-group",
#         "custom": {
#             "name": "somename",
#             "labels": {},
#             "blocks": {
#                 "position1": {
#                     "data": {
#                         "custom": {
#                             "classes": [],
#                             "content": [],
#                             "engine": None,
#                             "labels": {},
#                         },
#                         "type": "block",
#                     },
#                     "info": {
#                         "context": {
#                             "end_column": 0,
#                             "end_line": 0,
#                             "source": None,
#                             "start_column": 0,
#                             "start_line": 0,
#                         },
#                         "named_args": {},
#                         "subtype": None,
#                         "tags": [],
#                         "unnamed_args": [],
#                     },
#                 },
#                 "position2": {
#                     "data": {
#                         "custom": {
#                             "classes": [],
#                             "content": [],
#                             "engine": None,
#                             "labels": {},
#                         },
#                         "type": "block",
#                     },
#                     "info": {
#                         "context": {
#                             "end_column": 0,
#                             "end_line": 0,
#                             "source": None,
#                             "start_column": 0,
#                             "start_line": 0,
#                         },
#                         "named_args": {},
#                         "subtype": None,
#                         "tags": [],
#                         "unnamed_args": [],
#                     },
#                 },
#             },
#         },
#     }
