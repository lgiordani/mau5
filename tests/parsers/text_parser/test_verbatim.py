# from mau.lexers.text_lexer import TextLexer
# from mau.nodes.inline import TextNodeData, VerbatimNodeData
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
# def test_verbatim():
#     source = "`Many different words`"
# 
#     expected = [
#         Node(
#             data=VerbatimNodeData("Many different words"),
#             info=NodeInfo(context=generate_context(0, 0, 0, 22)),
#         ),
#     ]
# 
#     assert runner(source).nodes == expected
# 
# 
# def test_verbatim_escaped_backtick():
#     source = r"`\``"
# 
#     expected = [
#         Node(
#             data=VerbatimNodeData("`"),
#             info=NodeInfo(context=generate_context(0, 0, 0, 4)),
#         )
#     ]
# 
#     assert runner(source).nodes == expected
# 
# 
# def test_verbatim_style_inside_verbatim():
#     source = r"`_Many different words_`"
# 
#     expected = [
#         Node(
#             data=VerbatimNodeData("_Many different words_"),
#             info=NodeInfo(context=generate_context(0, 0, 0, 24)),
#         ),
#     ]
# 
#     assert runner(source).nodes == expected
# 
# 
# def test_verbatim_open():
#     source = r"`Many different words"
# 
#     expected = [
#         Node(
#             data=TextNodeData("`Many different words"),
#             info=NodeInfo(context=generate_context(0, 0, 0, 21)),
#         ),
#     ]
# 
#     assert runner(source).nodes == expected
# 
# 
# def test_verbatim_escape_characters():
#     source = r"`$Many$ %different% \words`"
# 
#     expected = [
#         Node(
#             data=VerbatimNodeData(r"$Many$ %different% \words"),
#             info=NodeInfo(context=generate_context(0, 0, 0, 27)),
#         ),
#     ]
# 
#     assert runner(source).nodes == expected
