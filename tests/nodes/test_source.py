# from mau.nodes.source import (
#     SourceLineNodeData,
#     SourceMarkerNodeContext,
#     SourceNodeData,
# )


# def test_source_node_content():
#     node_content = SourceNodeData("somelanguage")

#     assert node_content.type == "source"
#     assert node_content.asdict() == {
#         "type": "source",
#         "language": "somelanguage",
#     }


# def test_source_line_node_content():
#     node_content = SourceLineNodeData("42", "somecontent")

#     assert node_content.type == "source-line"
#     assert node_content.asdict() == {
#         "type": "source-line",
#         "line_number": "42",
#         "line_content": "somecontent",
#         "highlight_style": None,
#     }


# def test_source_line_marker_node_content():
#     node_content = SourceMarkerNodeContext("somemarker")

#     assert node_content.type == "source-marker"
#     assert node_content.asdict() == {"type": "source-marker", "value": "somemarker"}
