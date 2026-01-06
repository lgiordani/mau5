# from mau.test_helpers import check_node_data_with_content
# from mau.nodes.command import TocItemNodeData, TocNodeData


# def test_toc_node_content():
#     node_content = TocNodeData()

#     assert node_content.type == "toc"
#     assert node_content.asdict() == {
#         "type": "toc",
#         "nested_entries": [],
#         "plain_entries": [],
#     }


# def test_toc_item_node_content():
#     node_content = TocItemNodeData(level=1, internal_id="someid")

#     assert node_content.type == "toc-item"
#     assert list(node_content.allowed_keys.keys()) == ["text", "entries"]
#     assert node_content.level == 1
#     assert node_content.internal_id == "someid"
#     assert node_content.asdict() == {
#         "type": "toc-item",
#         "level": 1,
#         "internal_id": "someid",
#         "text": [],
#         "entries": [],
#     }
