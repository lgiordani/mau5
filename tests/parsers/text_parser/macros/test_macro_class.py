# import pytest
# 
# from mau.lexers.text_lexer import TextLexer
# from mau.nodes.inline import StyleNodeData, TextNodeData, VerbatimNodeData
# from mau.nodes.macros import MacroClassNodeData
# from mau.nodes.node import Node, NodeInfo
# from mau.parsers.base_parser import MauParserException
# from mau.parsers.text_parser import TextParser
# from mau.test_helpers import (
#     compare_asdict_list,
#     generate_context,
#     init_parser_factory,
#     parser_runner_factory,
# )
# 
# init_parser = init_parser_factory(TextLexer, TextParser)
# 
# runner = parser_runner_factory(TextLexer, TextParser)
# 
# 
# def test_macro_class_with_single_class():
#     source = '[class]("text with that class", classname)'
# 
#     expected_nodes = [
#         Node(
#             data=MacroClassNodeData(
#                 ["classname"],
#                 content=[
#                     Node(
#                         data=TextNodeData("text with that class"),
#                         info=NodeInfo(context=generate_context(0, 9, 0, 29)),
#                     )
#                 ],
#             ),
#             info=NodeInfo(context=generate_context(0, 0, 0, 42)),
#         ),
#     ]
# 
#     parser = runner(source)
# 
#     compare_asdict_list(parser.nodes, expected_nodes)
# 
# 
# def test_macro_class_with_multiple_classes():
#     source = '[class]("text with that class", classname1, classname2)'
# 
#     expected_nodes = [
#         Node(
#             data=MacroClassNodeData(
#                 ["classname1", "classname2"],
#                 content=[
#                     Node(
#                         data=TextNodeData("text with that class"),
#                         info=NodeInfo(context=generate_context(0, 9, 0, 29)),
#                     )
#                 ],
#             ),
#             info=NodeInfo(context=generate_context(0, 0, 0, 55)),
#         ),
#     ]
# 
#     parser = runner(source)
# 
#     compare_asdict_list(parser.nodes, expected_nodes)
# 
# 
# def test_macro_class_with_rich_text():
#     source = '[class]("Some text with `verbatim words` and _styled ones_", classname)'
# 
#     expected_nodes = [
#         Node(
#             data=MacroClassNodeData(
#                 ["classname"],
#                 content=[
#                     Node(
#                         data=TextNodeData("Some text with "),
#                         info=NodeInfo(context=generate_context(0, 9, 0, 24)),
#                     ),
#                     Node(
#                         data=VerbatimNodeData("verbatim words"),
#                         info=NodeInfo(context=generate_context(0, 24, 0, 40)),
#                     ),
#                     Node(
#                         data=TextNodeData(" and "),
#                         info=NodeInfo(context=generate_context(0, 40, 0, 45)),
#                     ),
#                     Node(
#                         data=StyleNodeData(
#                             "underscore",
#                             content=[
#                                 Node(
#                                     data=TextNodeData("styled ones"),
#                                     info=NodeInfo(
#                                         context=generate_context(0, 46, 0, 57)
#                                     ),
#                                 )
#                             ],
#                         ),
#                         info=NodeInfo(context=generate_context(0, 45, 0, 58)),
#                     ),
#                 ],
#             ),
#             info=NodeInfo(context=generate_context(0, 0, 0, 71)),
#         ),
#     ]
# 
#     parser = runner(source)
# 
#     compare_asdict_list(parser.nodes, expected_nodes)
# 
# 
# def test_macro_class_without_classes():
#     source = '[class]("text with that class")'
# 
#     expected_nodes = [
#         Node(
#             data=MacroClassNodeData(
#                 [],
#                 content=[
#                     Node(
#                         data=TextNodeData("text with that class"),
#                         info=NodeInfo(context=generate_context(0, 9, 0, 29)),
#                     )
#                 ],
#             ),
#             info=NodeInfo(context=generate_context(0, 0, 0, 31)),
#         ),
#     ]
# 
#     parser = runner(source)
# 
#     compare_asdict_list(parser.nodes, expected_nodes)
# 
# 
# def test_macro_class_without_text():
#     source = "[class]()"
# 
#     with pytest.raises(MauParserException) as exc:
#         runner(source)
# 
#     assert exc.value.context == generate_context(0, 0, 0, 9)
