# from mau.nodes.document import (
#     DocumentNode,
#     HorizontalRuleNode,
# )


# def test_horizontal_rule_node():
#     node = HorizontalRuleNode()

#     assert node.type == "horizontal_rule"
#     assert node.asdict() == {
#         "type": "horizontal_rule",
#         "custom": {
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


# def test_document_node():
#     node = DocumentNode()

#     assert node.type == "document"
#     assert node.asdict() == {
#         "type": "document",
#         "custom": {
#             "content": [],
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
