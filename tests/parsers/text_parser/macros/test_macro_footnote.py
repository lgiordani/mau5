# import pytest
# 
# from mau.lexers.text_lexer import TextLexer
# from mau.nodes.footnotes import FootnoteNodeData
# from mau.nodes.macros import MacroFootnoteNodeData
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
# def test_macro_footnote():
#     source = "[footnote](notename)"
# 
#     footnote_data = FootnoteNodeData(name="notename")
# 
#     footnote_node = Node(
#         data=MacroFootnoteNodeData(footnote=footnote_data),
#         info=NodeInfo(context=generate_context(0, 0, 0, 20)),
#     )
# 
#     parser = runner(source)
# 
#     compare_asdict_list(parser.nodes, [footnote_node])
#     compare_asdict_list(parser.footnotes, [footnote_data])
# 
# 
# def test_macro_footnote_without_name():
#     source = "[footnote]()"
# 
#     with pytest.raises(MauParserException) as exc:
#         runner(source)
# 
#     assert exc.value.context == generate_context(0, 0, 0, 12)
