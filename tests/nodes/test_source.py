# from mau.nodes.source import (
#     SourceLineNode,
#     SourceMarkerNode,
#     SourceNode,
# )


# def test_source_line_marker_node():
#     node = SourceMarkerNode("somemarker")

#     assert node.type == "source-marker"
#     assert node.asdict() == {
#         "type": "source-marker",
#         "custom": {
#             "value": "somemarker",
#         },
#         "info": {
#             "context": {
#                 "end_column": 0,
#                 "end_line": 0,
#                 "source": None,
#                 "start_column": 0,
#                 "start_line": 0,
#             },
#             "named_args": {},
#             "subtype": None,
#             "tags": [],
#             "unnamed_args": [],
#         },
#     }


# def test_source_node():
#     node = SourceNode("somelanguage")

#     assert node.type == "source"
#     assert node.asdict() == {
#         "type": "source",
#         "custom": {
#             "language": "somelanguage",
#             "content": [],
#             "labels": {},
#         },
#         "info": {
#             "context": {
#                 "end_column": 0,
#                 "end_line": 0,
#                 "source": None,
#                 "start_column": 0,
#                 "start_line": 0,
#             },
#             "named_args": {},
#             "subtype": None,
#             "tags": [],
#             "unnamed_args": [],
#         },
#     }


# def test_source_line_node():
#     node = SourceLineNode("42", "somecontent")

#     assert node.type == "source-line"
#     assert node.asdict() == {
#         "type": "source-line",
#         "custom": {
#             "line_number": "42",
#             "line_content": "somecontent",
#             "highlight_style": None,
#         },
#         "info": {
#             "context": {
#                 "end_column": 0,
#                 "end_line": 0,
#                 "source": None,
#                 "start_column": 0,
#                 "start_line": 0,
#             },
#             "named_args": {},
#             "subtype": None,
#             "tags": [],
#             "unnamed_args": [],
#         },
#     }


# def test_source_line_node_with_marker():
#     marker_node = SourceMarkerNode("somemarker")
#     node = SourceLineNode("42", "somecontent", marker=marker_node)

#     assert node.type == "source-line"
#     assert node.asdict() == {
#         "type": "source-line",
#         "custom": {
#             "line_number": "42",
#             "line_content": "somecontent",
#             "highlight_style": None,
#             "marker": {
#                 "type": "source-marker",
#                 "custom": {
#                     "value": "somemarker",
#                 },
#                 "info": {
#                     "context": {
#                         "end_column": 0,
#                         "end_line": 0,
#                         "source": None,
#                         "start_column": 0,
#                         "start_line": 0,
#                     },
#                     "named_args": {},
#                     "subtype": None,
#                     "tags": [],
#                     "unnamed_args": [],
#                 },
#             },
#         },
#         "info": {
#             "context": {
#                 "end_column": 0,
#                 "end_line": 0,
#                 "source": None,
#                 "start_column": 0,
#                 "start_line": 0,
#             },
#             "named_args": {},
#             "subtype": None,
#             "tags": [],
#             "unnamed_args": [],
#         },
#     }
