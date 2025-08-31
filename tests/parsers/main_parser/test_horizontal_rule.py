# from mau.lexers.document_lexer import DocumentLexer
# from mau.nodes.page import HorizontalRuleNode
# from mau.parsers.document_parser import DocumentParser

# from mau.test_helpers import init_parser_factory, parser_runner_factory

# init_parser = init_parser_factory(DocumentLexer, DocumentParser)

# runner = parser_runner_factory(DocumentLexer, DocumentParser)


# def test_horizontal_rule():
#     source = "---"

#     expected = [HorizontalRuleNode()]

#     assert runner(source).nodes == expected


# def test_horizontal_rule_with_arguments():
#     source = """
#     [*break,arg1,key1=value1]
#     ---
#     """

#     expected = [
#         HorizontalRuleNode(
#             subtype="break",
#             args=["arg1"],
#             kwargs={
#                 "key1": "value1",
#             },
#         ),
#     ]

#     assert runner(source).nodes == expected
