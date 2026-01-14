# import pytest
# 
# from mau.lexers.text_lexer import TextLexer
# from mau.nodes.macros import MacroImageNodeData
# from mau.nodes.node import Node, NodeInfo
# from mau.parsers.base_parser import MauParserException
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
# def test_macro_image():
#     source = "[image](/the/path.jpg)"
# 
#     expected = [
#         Node(
#             data=MacroImageNodeData("/the/path.jpg"),
#             info=NodeInfo(context=generate_context(0, 0, 0, 22)),
#         ),
#     ]
# 
#     assert runner(source).nodes == expected
# 
# 
# def test_macro_image_with_alt_text():
#     source = '[image](/the/path.jpg, "alt name")'
# 
#     expected = [
#         Node(
#             data=MacroImageNodeData("/the/path.jpg", alt_text="alt name"),
#             info=NodeInfo(context=generate_context(0, 0, 0, 34)),
#         ),
#     ]
# 
#     assert runner(source).nodes == expected
# 
# 
# def test_macro_image_with_width_and_height():
#     source = "[image](/the/path.jpg, width=1200, height=600)"
# 
#     expected = [
#         Node(
#             data=MacroImageNodeData(
#                 "/the/path.jpg", alt_text=None, width="1200", height="600"
#             ),
#             info=NodeInfo(context=generate_context(0, 0, 0, 46)),
#         ),
#     ]
# 
#     assert runner(source).nodes == expected
# 
# 
# def test_macro_image_without_uri():
#     source = "[image]()"
# 
#     with pytest.raises(MauParserException) as exc:
#         runner(source)
# 
#     assert exc.value.context == generate_context(0, 0, 0, 9)
