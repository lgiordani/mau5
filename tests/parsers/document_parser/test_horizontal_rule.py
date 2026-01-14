# from mau.environment.environment import Environment
# from mau.lexers.document_lexer import DocumentLexer
# from mau.nodes.document import HorizontalRuleNodeData
# from mau.nodes.inline import TextNodeData
# from mau.nodes.node import Node, NodeInfo
# from mau.parsers.document_parser import DocumentParser
# from mau.test_helpers import (
#     compare_asdict_list,
#     generate_context,
#     init_parser_factory,
#     parser_runner_factory,
# )
# 
# init_parser = init_parser_factory(DocumentLexer, DocumentParser)
# 
# runner = parser_runner_factory(DocumentLexer, DocumentParser)
# 
# 
# def test_horizontal_rule():
#     source = """
#     ---
#     """
# 
#     expected_nodes = [
#         Node(
#             data=HorizontalRuleNodeData(),
#             info=NodeInfo(context=generate_context(1, 0, 1, 3)),
#         )
#     ]
# 
#     parser = runner(source)
# 
#     compare_asdict_list(parser.nodes, expected_nodes)
# 
# 
# def test_horizontal_rule_with_arguments():
#     source = """
#     [arg1,#tag1,*subtype1,key1=value1]
#     ---
#     """
# 
#     expected_nodes = [
#         Node(
#             data=HorizontalRuleNodeData(),
#             info=NodeInfo(
#                 unnamed_args=["arg1"],
#                 named_args={
#                     "key1": "value1",
#                 },
#                 tags=["tag1"],
#                 subtype="subtype1",
#                 context=generate_context(2, 0, 2, 3),
#             ),
#         )
#     ]
# 
#     parser = runner(source)
# 
#     compare_asdict_list(parser.nodes, expected_nodes)
# 
# 
# def test_horizontal_rule_with_labels():
#     source = """
#     .details This is a label
#     ---
#     """
# 
#     expected_nodes = [
#         Node(
#             data=HorizontalRuleNodeData(
#                 labels={
#                     "details": [
#                         Node(
#                             data=TextNodeData("This is a label"),
#                             info=NodeInfo(
#                                 context=generate_context(1, 9, 1, 24),
#                             ),
#                         )
#                     ]
#                 }
#             ),
#             info=NodeInfo(
#                 context=generate_context(2, 0, 2, 3),
#             ),
#         )
#     ]
# 
#     parser = runner(source)
# 
#     compare_asdict_list(parser.nodes, expected_nodes)
# 
# 
# def test_horizontal_rule_with_control():
#     environment = Environment()
#     environment["answer"] = "24"
# 
#     source = """
#     @if answer==42
#     [arg1, arg2]
#     . Some title
#     ---
#     """
# 
#     parser = runner(source, environment)
# 
#     compare_asdict_list(parser.nodes, [])
# 
#     assert parser.arguments_buffer.arguments is None
#     assert parser.label_buffer.labels == {}
#     assert parser.control_buffer.control is None
