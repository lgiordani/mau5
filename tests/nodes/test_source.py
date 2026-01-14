# from mau.nodes.source import (
#     SourceLineNodeData,
#     SourceMarkerNodeData,
#     SourceNodeData,
# )
# 
# 
# def test_source_node_data():
#     node_content = SourceNodeData("somelanguage")
# 
#     assert node_content.type == "source"
#     assert node_content.asdict() == {
#         "type": "source",
#         "custom": {
#             "language": "somelanguage",
#             "content": [],
#         },
#     }
# 
# 
# def test_source_line_node_data():
#     node_content = SourceLineNodeData("42", "somecontent")
# 
#     assert node_content.type == "source-line"
#     assert node_content.asdict() == {
#         "type": "source-line",
#         "custom": {
#             "line_number": "42",
#             "line_content": "somecontent",
#             "highlight_style": None,
#         },
#     }
# 
# 
# def test_source_line_marker_node_data():
#     node_content = SourceMarkerNodeData("somemarker")
# 
#     assert node_content.type == "source-marker"
#     assert node_content.asdict() == {
#         "type": "source-marker",
#         "custom": {
#             "value": "somemarker",
#         },
#     }
