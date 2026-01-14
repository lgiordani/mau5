# from mau.lexers.text_lexer import TextLexer
# from mau.nodes.inline import StyleNodeData, TextNodeData
# from mau.nodes.node import Node, NodeInfo
# from mau.parsers.text_parser import TextParser
# from mau.test_helpers import (
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
# def test_underscore():
#     source = "_Some text_"
# 
#     expected_node = Node(
#         data=StyleNodeData(
#             "underscore",
#             content=[
#                 Node(
#                     data=TextNodeData("Some text"),
#                     info=NodeInfo(context=generate_context(0, 1, 0, 10)),
#                 )
#             ],
#         ),
#         info=NodeInfo(context=generate_context(0, 0, 0, 11)),
#     )
# 
#     assert runner(source).nodes == [expected_node]
# 
# 
# def test_star():
#     source = "*Some text*"
# 
#     expected_node = Node(
#         data=StyleNodeData(
#             "star",
#             content=[
#                 Node(
#                     data=TextNodeData("Some text"),
#                     info=NodeInfo(context=generate_context(0, 1, 0, 10)),
#                 )
#             ],
#         ),
#         info=NodeInfo(context=generate_context(0, 0, 0, 11)),
#     )
# 
#     assert runner(source).nodes == [expected_node]
# 
# 
# def test_caret():
#     source = "^Some text^"
# 
#     expected_node = Node(
#         data=StyleNodeData(
#             "caret",
#             content=[
#                 Node(
#                     data=TextNodeData("Some text"),
#                     info=NodeInfo(context=generate_context(0, 1, 0, 10)),
#                 )
#             ],
#         ),
#         info=NodeInfo(context=generate_context(0, 0, 0, 11)),
#     )
# 
#     assert runner(source).nodes == [expected_node]
# 
# 
# def test_tilde():
#     source = "~Some text~"
# 
#     expected_node = Node(
#         data=StyleNodeData(
#             "tilde",
#             content=[
#                 Node(
#                     data=TextNodeData("Some text"),
#                     info=NodeInfo(context=generate_context(0, 1, 0, 10)),
#                 )
#             ],
#         ),
#         info=NodeInfo(context=generate_context(0, 0, 0, 11)),
#     )
# 
#     assert runner(source).nodes == [expected_node]
# 
# 
# def test_style_within_style():
#     source = "_*Words with two styles*_"
# 
#     expected_node = Node(
#         data=StyleNodeData(
#             "underscore",
#             content=[
#                 Node(
#                     data=StyleNodeData(
#                         "star",
#                         content=[
#                             Node(
#                                 data=TextNodeData("Words with two styles"),
#                                 info=NodeInfo(context=generate_context(0, 2, 0, 23)),
#                             )
#                         ],
#                     ),
#                     info=NodeInfo(context=generate_context(0, 1, 0, 24)),
#                 )
#             ],
#         ),
#         info=NodeInfo(context=generate_context(0, 0, 0, 25)),
#     )
# 
#     assert runner(source).nodes == [expected_node]
# 
# 
# def test_double_style_cancels_itself():
#     source = "__Text__"
# 
#     expected = [
#         Node(
#             data=StyleNodeData("underscore"),
#             info=NodeInfo(context=generate_context(0, 0, 0, 2)),
#         ),
#         Node(
#             data=TextNodeData("Text"),
#             info=NodeInfo(context=generate_context(0, 2, 0, 6)),
#         ),
#         Node(
#             data=StyleNodeData("underscore"),
#             info=NodeInfo(context=generate_context(0, 6, 0, 8)),
#         ),
#     ]
# 
#     assert runner(source).nodes == expected
# 
# 
# def test_mix_text_and_styles():
#     source = "Some text _and style_ and *more style* here"
# 
#     expected = [
#         Node(
#             data=TextNodeData("Some text "),
#             info=NodeInfo(context=generate_context(0, 0, 0, 10)),
#         ),
#         Node(
#             data=StyleNodeData(
#                 "underscore",
#                 content=[
#                     Node(
#                         data=TextNodeData("and style"),
#                         info=NodeInfo(context=generate_context(0, 11, 0, 20)),
#                     )
#                 ],
#             ),
#             info=NodeInfo(context=generate_context(0, 10, 0, 21)),
#         ),
#         Node(
#             data=TextNodeData(" and "),
#             info=NodeInfo(context=generate_context(0, 21, 0, 26)),
#         ),
#         Node(
#             data=StyleNodeData(
#                 "star",
#                 content=[
#                     Node(
#                         data=TextNodeData("more style"),
#                         info=NodeInfo(context=generate_context(0, 27, 0, 37)),
#                     )
#                 ],
#             ),
#             info=NodeInfo(context=generate_context(0, 26, 0, 38)),
#         ),
#         Node(
#             data=TextNodeData(" here"),
#             info=NodeInfo(context=generate_context(0, 38, 0, 43)),
#         ),
#     ]
# 
#     assert runner(source).nodes == expected
# 
# 
# def test_unclosed_style():
#     source = "_Text"
# 
#     expected = [
#         Node(
#             data=TextNodeData("_Text"),
#             info=NodeInfo(context=generate_context(0, 0, 0, 5)),
#         ),
#     ]
# 
#     assert runner(source).nodes == expected
