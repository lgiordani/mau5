# from mau.environment.environment import Environment
# from mau.lexers.document_lexer import DocumentLexer
# from mau.nodes.document import DocumentNodeData
# from mau.nodes.inline import TextNodeData
# from mau.nodes.node import Node, NodeInfo
# from mau.nodes.paragraph import ParagraphLineNodeData, ParagraphNodeData
# from mau.parsers.document_parser import DocumentParser
# from mau.test_helpers import (
#     compare_asdict_list,
#     compare_asdict_object,
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
# def test_parse_discards_empty_lines():
#     source = "\n\n\n\n"
# 
#     parser = runner(source)
# 
#     compare_asdict_list(parser.nodes, [])
# 
# 
# def test_parse_output():
#     source = ""
# 
#     assert runner(source).output == {
#         "document": None,
#         "nested_toc": None,
#         "plain_toc": None,
#     }
# 
# 
# def test_parse_output_custom_content_container():
#     source = "text"
# 
#     class CustomDocumentNodeData(DocumentNodeData):
#         type = "custom-document"
# 
#     environment = Environment()
#     environment["mau.parser.document_wrapper"] = CustomDocumentNodeData
# 
#     compare_asdict_object(
#         runner(source, environment).output["document"],
#         Node(
#             data=CustomDocumentNodeData(
#                 content=[
#                     Node(
#                         data=ParagraphNodeData(
#                             content=[
#                                 Node(
#                                     data=ParagraphLineNodeData(
#                                         content=[
#                                             Node(
#                                                 data=TextNodeData("text"),
#                                                 info=NodeInfo(
#                                                     context=generate_context(0, 0, 0, 4)
#                                                 ),
#                                             )
#                                         ]
#                                     ),
#                                     info=NodeInfo(context=generate_context(0, 0, 0, 4)),
#                                 )
#                             ]
#                         ),
#                         info=NodeInfo(context=generate_context(0, 0, 0, 4)),
#                     )
#                 ]
#             ),
#             info=NodeInfo(context=generate_context(0, 0, 0, 4)),
#         ),
#     )
